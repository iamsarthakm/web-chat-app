//Authentication

const mongoose = require("mongoose");

module.exports.checkLogin = function(req, res, next) {
  if (!req.user && !req.session.user) {
    res.redirect("/user/login");
  } else {
    next();
  }
};

module.exports.loggedIn = function(req, res, next) {
  if (!req.user && !req.session.user) {
    next();
  } else {
    res.redirect("/chat");
  }
};


//validation

//requiring dependencies.
const mongoose = require("mongoose");

const userModel = mongoose.model("User");

//router level middleware for checking existing user.
module.exports.emailExist = function(req, res, next) {
  userModel.findOne({ email: req.body.email }, function(err, result) {
    if (err) {
      res.render("message", {
        title: "Error",
        msg: "Some Error Occured During Email Checking.",
        status: 500,
        error: err,
        user: req.session.user
      });
    } else if (result) {
      res.render("message", {
        title: "Error",
        msg: "User Already Exist",
        status: 500,
        error: "",
        user: req.session.user
      });
    } else {
      next();
    }
  });
};



// sending and recieving messages


 //sending message.
 $('form').submit(function(){
    socket.emit('chat-msg',{msg:$('#myMsg').val(),msgTo:toUser,date:Date.now()});
    $('#myMsg').val("");
    $('#sendBtn').hide();
    return false;
  }); //end of sending message.

  //receiving if disctrating found
  socket.on('distracting',function(data){
    console.log('dis',data);
    var elemet =document.getElementById(data.id);
    elemet.style.background='lightcoral';
    /*elemet.style.opacity = "0.1";*/
    document.getElementById(data.id).innerHTML ="This is a Distracting message. Reload or click again to check the message.";
  })
  socket.on('chat-msg',function(data){
    //styling of chat message.
    var chatDate = moment(data.date).format("MMMM Do YYYY, hh:mm:ss a");
    var txt1 = $('<span></span>').text(data.msgFrom+" : ").css({"color":"#006080"});
    var txt2 = $('<span></span>').text(chatDate).css({"float":"right","color":"#a6a6a6","font-size":"16px"});
    var txt3 = $('<p></p>').append(txt1,txt2);
    var txt4 = $('<p></p>').text(data.msg).css({"color":"#000000"});
    //showing chat in chat box.
    $('#messages').append($(`<li id=${data.date} class="mm">`).append(txt3,txt4));
      msgCount++;
      console.log(msgCount);
      $('#typing').text("");
      $('#scrl2').scrollTop($('#scrl2').prop("scrollHeight"));
  }); //end of receiving messages.

  //on disconnect event.
  //passing data on connection.


