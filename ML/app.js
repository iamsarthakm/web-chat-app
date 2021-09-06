var express = require('express');
var http = require('http');
var path = require("path");
var bodyParser = require('body-parser');
var helmet = require('helmet');
var rateLimit = require("express-rate-limit");
var fileupload = require("express-fileupload");
var request=require('request');
var multer = require('multer');
var upload = multer({ dest: 'uploads/' });
var util = require('util');
var exec = require('child_process').exec;


var app = express();
var server = http.createServer(app);

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname,'./public')));
app.use(helmet());
app.use(limiter);

const storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, 'uploads/');
	},
  
	// By default, multer removes file extensions so let's add them back
	filename: function(req, file, cb) {
		cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
	}
  });

var globalmessage="";
var globaltranslated="";
var globalpred=0;
var file_path;
var userid;

app.get('/', function(req,res){
  res.sendFile(path.join(__dirname,'./public/index.html'));
});

app.post('/predict_text', function(req,res){
	globalmessage= req.body.message;
	userid=req.body.userid;

	var path='http://127.0.0.1:8080/predict_text?api_key=admin123admin';
	path+="&userid="+userid;
	urlAdd=encodeURI(path);
	var json_obj={"message":globalmessage};
	request({url: urlAdd,
		method: "POST",
		json: json_obj
		}, function (error, response, body) {
		globalpred=body.pred;
		
		console.log(globalpred)
		res.render('results',{textlab:globalmessage, translat:globaltranslated, prediction:globalpred});
	});
});

app.post('/predict_audio', function(req,res){
	var curl_out;
	let upload = multer({ storage: storage }).single('audio_file');

  	upload(req, res, function(err) {
      // req.file contains information of uploaded file
	  // req.body contains information of text fields, if there were any
	  userid=req.body.userid2;

      if (req.fileValidationError) {
          return res.send(req.fileValidationError);
      }
      else if (!req.file) {
          return res.send('Please select an audio file to upload');
      }
      else if (err instanceof multer.MulterError) {
          return res.send(err);
      }
      else if (err) {
          return res.send(err);
	  }
	  file_path = req.file.path;

	var path='http://127.0.0.1:8080/predict_audio?api_key=admin123admin';
	path+="&userid="+userid;
	urlAdd=encodeURI(path);

	var command = `curl -F "file=@${file_path}; type=audio/flac" "${urlAdd}"`;

	child = exec(command, function(error, stdout, stderr){

	if(error !== null)
	{
		console.log('exec error: ' + error);
	}

	curl_out=JSON.parse(stdout);

	globalmessage=curl_out.msg;
	globalpred=curl_out.pred;
	if(curl_out.hasOwnProperty("msg_translation"))
		globaltranslated=curl_out.msg_translation;
	else
		globaltranslated=globalmessage;

	res.render('results',{textlab:globalmessage, translat: globaltranslated, prediction:globalpred});
	});
});
});

app.post('/train', function(req,res){
	var feed=req.body.feedback;
	if(feed=="no")
	{
	var path='http://127.0.0.1:8080/train?api_key=admin123admin&message=';
	path+=globaltranslated+"&feedback="+(1-(globalpred))+"&userid="+userid;
	urlAdd=encodeURI(path);
	request(urlAdd, function (error, response, body) {
		res.send("<html><head><title>Rectified</title></head><body><fieldset><h3>Thank you! We will rectify the model</h3></fieldset></body></html>");
	  });
	}
	else{
		res.send("<html><head><title>Thank You</title></head><body><fieldset><h3>Thank you! Glad to hear that!</h3></fieldset></body></html>");
	}
});

app.post('/quit', function(req, res){
	var path='http://127.0.0.1:8080/quit?api_key=admin123admin';
	urlAdd=encodeURI(path);
	request(urlAdd, function (error, response, body) {
		res.send("<html><head><title>Quit</title></head><body><fieldset><h3>Thank you! You have closed the service! </h3></fieldset></body></html>");
	});
});

app.listen(process.env.PORT || 3000, function() { 
	console.log("server running on port 3000 in %s mode", app.settings.env);
});