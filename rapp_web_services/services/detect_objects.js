/*!
 * @file detect_obects.service.js
 * @brief Image Recognition hop front-end service.
 *
 */


/**
 *  MIT License (MIT)
 *
 *  Copyright (c) <2014> <Rapp Project EU>
 *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy
 *  of this software and associated documentation files (the "Software"), to deal
 *  in the Software without restriction, including without limitation the rights
 *  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *  copies of the Software, and to permit persons to whom the Software is
 *  furnished to do so, subject to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be included in
 *  all copies or substantial portions of the Software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 *  THE SOFTWARE.
 *
 *
 *  Authors: Konstantinos Panayiotou
 *  Contact: klpanagi@gmail.com
 *
 */



//"use strict";



/* ------------< Load and set basic configuration parameters >-------------*/
var __DEBUG__ = false;
var user = process.env.LOGNAME;
var module_path = '../modules/';
var config_path = '../config/';
var srvEnv = require( config_path + 'env/hop-services.json' )
var __hopServiceName = 'detect_objects';
var __hopServiceId = null;
var __masterId = null;
var __cacheDir = '~/.hop/cache/services/';
/* ----------------------------------------------------------------------- */

/* --------------------------< Load required modules >---------------------*/
var Fs = require( module_path + 'fileUtils.js' );
var hop = require('hop');
var RandStringGen = require ( module_path +
  'RandomStrGenerator/randStringGen.js' );
var RosSrvPool = require(module_path + 'ros/srvPool.js');
var RosParam = require(module_path + 'ros/rosParam.js')
/* ----------------------------------------------------------------------- */

var script_dir_path = __dirname;
var script_full_pah = __filename;
var rapp_image_recognition_path = script_dir_path +
  "/../../rapp_image_recognition/";
var data_path = rapp_image_recognition_path + "data/book_1/";
//console.log(data_path)

var ros_service_name = srvEnv[__hopServiceName].ros_srv_name;
var rosParam = new RosParam({});
var rosSrvThreads = 0;  // Default is set at zero (0)

/* -------------------------< ROS service pool >-------------------------- */
var rosSrvPool = undefined;

rosParam.getParam_async('/rapp_qr_detection_threads', function(data){
  if(data > 0)
  {
    rosSrvThreads = data;
    rosSrvPool = new RosSrvPool(ros_service_name, rosSrvThreads);
  }
});
/* ----------------------------------------------------------------------- */

/*----<Random String Generator configurations---->*/
var stringLength = 5;
var randStrGen = new RandStringGen( stringLength );
/*------------------------------------------------*/

/* ------< Set timer values for websocket communication to rosbridge> ----- */
var timeout = srvEnv[__hopServiceName].timeout; // ms
var max_tries = 3;
/* ----------------------------------------------------------------------- */

register_master_interface();


/*!
 * @brief Face Detection HOP Service Core.
 *
 * @param file_uri Path of uploaded image file. Returned by hop server.
 * @return Message response from faceDetection ROS Service.
 *
 */
service detect_objects ( {file_uri:'', limit: ''} )
{
  var startT = new Date().getTime();
  var execTime = 0;
  if(rosSrvThreads) {var rosSrvCall = rosSrvPool.getAvailable();}
  else {var rosSrvCall = ros_service_name;}
  console.log(rosSrvCall);
  postMessage( craft_slaveMaster_msg('log', 'client-request {' + rosSrvCall + '}') );

  var logMsg = 'Image stored at [' + file_uri + ']';
  postMessage( craft_slaveMaster_msg('log', logMsg) );

  /* --< Perform renaming on the reived file. Add uniqueId value> --- */
  var unqCallId = randStrGen.createUnique();
  var fileUrl = file_uri.split('/');
  var fileName = fileUrl[fileUrl.length -1];

  var cpFilePath = __cacheDir + fileName.split('.')[0] + '-'  + unqCallId +
    '.' + fileName.split('.')[1];

  cpFilePath = Fs.resolve_path(cpFilePath);
  /* ---------------------------------------------------------------- */

  /* --------------------- Handle transferred file ------------------------- */
  if (Fs.renameFile(file_uri, cpFilePath) == false)
  {
    //could not rename file. Probably cannot access the file. Return to client!
    var logMsg = 'Failed to rename file: [' + file_uri + '] --> [' +
      cpFilePath + ']';
    console.log(logMsg);

    postMessage( craft_slaveMaster_msg('log', logMsg) );
    Fs.rmFile(file_uri);
    randStrGen.removeCached(unqCallId);
    var resp_msg = craft_error_response();
    execTime = new Date().getTime() - startT;
    postMessage( craft_slaveMaster_msg('execTime', execTime) );
    return hop.HTTPResponseJson(resp_msg);
  }
  logMsg = 'Created copy of file ' + file_uri + ' at ' + cpFilePath;
  postMessage( craft_slaveMaster_msg('log', logMsg) );
  /*-------------------------------------------------------------------------*/


  // Asynchronous Response. Implementation
  /*----------------------------------------------------------------- */
  return hop.HTTPResponseAsync(
    function( sendResponse ) {

     var files = [];
     /* Add parameters hardcoded */
     var names = [
       'cat', 'cow', 'goat', 'hen', 'pig', 'sheep', 'cock',
       'dog', 'goose', 'horse', 'rabbit', 'turkey'
     ];

     for (var n in names)
     {
       files.push(data_path + names[n] + '.jpg');
     }

     var args = {
       /* Image path to perform faceDetection, used as input to the
        *  Face Detection ROS Node Service
        */
       "fname": cpFilePath,
       "limit": parseInt(limit),
       "names": names,
       "files": files
     };

/*=============================TEMPLATE======================================================*/
      var respFlag = false;
      var wsError = false;
      var rosbridge_msg = craft_rosbridge_msg(args, ros_service_name, unqCallId);

      /**
       * ---- Catch exception on initiating websocket.
       *  -- Return to client immediately on exception thrown.
       */
      try{
        var rosWS = new WebSocket('ws://localhost:9090');

        // Register WebSocket.onopen callback
        rosWS.onopen = function(){
          var logMsg = 'Connection to rosbridge established';
          postMessage( craft_slaveMaster_msg('log', logMsg) );
          this.send(JSON.stringify(rosbridge_msg));
        }
        // Register WebSocket.onclose callback
        rosWS.onclose = function(){
          var logMsg = 'Connection to rosbridge closed';
          postMessage( craft_slaveMaster_msg('log', logMsg) );
        }
        // Register WebSocket.message callback
        rosWS.onmessage = function(event){
          if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
          var logMsg = 'Received message from rosbridge';
          postMessage( craft_slaveMaster_msg('log', logMsg) );

          //console.log(event.value);
          Fs.rmFile(cpFilePath);
          respFlag = true; // Raise Response-Received Flag

          this.close(); // Close websocket
          rosWS = undefined; // Ensure deletion of websocket

          // Dismiss the unique call identity key for current client.
          randStrGen.removeCached( unqCallId );
          execTime = new Date().getTime() - startT;
          postMessage( craft_slaveMaster_msg('execTime', execTime) );
          var response = craft_response(event.value);
          sendResponse( hop.HTTPResponseJson(response));
        }
        rosWS.onerror = function(e){
          if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
          rosWS = undefined;
          wsError = true;

          var logMsg = 'Websocket' +
            'to rosbridge [ws//localhost:9090] got error...\r\n' + e;
          postMessage( craft_slaveMaster_msg('log', logMsg) );

          Fs.rmFile(cpFilePath);
          var response = craft_error_response();
          sendResponse( hop.HTTPResponseJson(response));
          execTime = new Date().getTime() - startT;
          postMessage( craft_slaveMaster_msg('execTime', execTime) );
        }
      }
      catch(e){
        if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
        rosWS = undefined;
        wsError = true;

        var logMsg = 'ERROR: Cannot open websocket' +
          'to rosbridge [ws//localhost:9090]\r\n' + e;
        postMessage( craft_slaveMaster_msg('log', logMsg) );

        Fs.rmFile(cpFilePath);
        var response = craft_error_response();
        sendResponse( hop.HTTPResponseJson(response));
        execTime = new Date().getTime() - startT;
        postMessage( craft_slaveMaster_msg('execTime', execTime) );
        return;
      }
      /*------------------------------------------------------------------ */

      var retries = 0;

      // Set Timeout wrapping function
      function asyncWrap(){
        setTimeout( function(){

         if (respFlag || wsError)
         {
           return;
         }
         else{
           retries += 1;

           var logMsg = 'Reached rosbridge response timeout' +
             '---> [' + timeout.toString() + '] ms ... Reconnecting to rosbridge.' +
             'Retry-' + retries;
           postMessage( craft_slaveMaster_msg('log', logMsg) );

           /* - Fail to receive message from rosbridge. Return to client */
           if (retries >= max_tries)
           {
             if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
             var logMsg = 'Reached max_retries [' + max_tries + ']' +
               ' Could not receive response from rosbridge...';
             postMessage( craft_slaveMaster_msg('log', logMsg) );

             Fs.rmFile(cpFilePath);

             rosWS.close();
             rosWS = undefined;
             //  Close websocket before return
             execTime = new Date().getTime() - startT;
             postMessage( craft_slaveMaster_msg('execTime', execTime) );
             var response = craft_error_response();
             sendResponse( hop.HTTPResponseJson(response));
             return;
           }

           if (rosWS != undefined)
           {
             rosWS.close();
           }
           rosWS = undefined;

           /* --------------< Re-open connection to the WebSocket >--------------*/
           try{
             rosWS = new WebSocket('ws://localhost:9090');

             /* -----------< Redefine WebSocket callbacks >----------- */
             rosWS.onopen = function(){
               var logMsg = 'Connection to rosbridge established';
               postMessage( craft_slaveMaster_msg('log', logMsg) );
               this.send(JSON.stringify(rosbridge_msg));
             }

             rosWS.onclose = function(){
               var logMsg = 'Connection to rosbridge closed';
               postMessage( craft_slaveMaster_msg('log', logMsg) );
             }

             rosWS.onmessage = function(event){
               if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
               var logMsg = 'Received message from rosbridge';
               postMessage( craft_slaveMaster_msg('log', logMsg) );

               //Remove the uniqueID so it can be reused
               randStrGen.removeCached( unqCallId );
               Fs.rmFile(cpFilePath);

               respFlag = true;
               execTime = new Date().getTime() - startT;
               postMessage( craft_slaveMaster_msg('execTime', execTime) );
               var response = craft_response(event.value);
               sendResponse( hop.HTTPResponseJson(response));
               this.close(); // Close websocket
               rosWS = undefined; // Decostruct websocket
             }
             rosWS.onerror = function(e){
               if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
               rosWS = undefined;
               wsError = true;

               var logMsg = 'Websocket' +
                 'to rosbridge [ws//localhost:9090] got error...\r\n' + e;
               postMessage( craft_slaveMaster_msg('log', logMsg) );

               Fs.rmFile(cpFilePath);
               var response = craft_error_response();
               sendResponse( hop.HTTPResponseJson(response));
               execTime = new Date().getTime() - startT;
               postMessage( craft_slaveMaster_msg('execTime', execTime) );
             }
           }
           catch(e){
             if(rosSrvThreads) {rosSrvPool.release(rosSrvCall);}
             rosWS = undefined;
             wsError = true;

             var logMsg = 'ERROR: Cannot open websocket' +
               'to rosbridge --> [ws//localhost:9090]';
             postMessage( craft_slaveMaster_msg('log', logMsg) );

             Fs.rmFile(cpFilePath);

             execTime = new Date().getTime() - startT;
             postMessage( craft_slaveMaster_msg('execTime', execTime) );
             var response = craft_error_response();
             sendResponse( hop.HTTPResponseJson(response));
             return;
           }

         }
         /*--------------------------------------------------------*/
         asyncWrap(); // Recall timeout function

       }, timeout); //Timeout value is set at 100 ms.
     }
     asyncWrap();
/*============================================================================*/
   }, this );
};


/*!
 * @brief Crafts the form/format for the message to be returned
 * @param rosbridge_msg Return message from ROS Service.
 * return Message to be returned from service.
 */
function craft_response(rosbridge_msg)
{
  var msg = JSON.parse(rosbridge_msg);
  var found_names = msg.values.found_names;
  var found_centers = msg.values.found_centers;
  var found_scores = msg.values.found_scores;
  var call_result = msg.result;
  var result = msg.values.result;
  //var error = msg.values.error;

  //console.log(msg);

  var crafted_msg = {found_names: [], found_scores: [],
    found_centers: [], error: '' };

  var logMsg = '';

  if (call_result)
  {
    for (var ii = 0; ii < found_names.length; ii++)
    {
      crafted_msg.found_names.push( found_names[ii] );
    }
    for (var ii = 0; ii < found_centers.length; ii++)
    {
      crafted_msg.found_centers.push( found_centers[ii].point );
    }
    for (var ii = 0; ii < found_scores.length; ii++)
    {
      crafted_msg.found_scores.push( found_scores[ii] );
    }
    crafted_msg.error = "";

    //TODO Add error message field to ROS service msg!!!!
    //if (error != '')
    //{
      //logMsg += ' ROS service [' + ros_service_name + '] error'
        //' ---> ' + error;
    //}
    //else
    //{
      //logMsg += ' ROS service [' + ros_service_name + '] returned with success'
    //}
  }
  else
  {
    logMsg = 'Communication with ROS service ' + ros_service_name +
      'failed. Unsuccesful call! Returning to client with error' +
      ' ---> RAPP Platform Failure';
    crafted_msg.error = "RAPP Platform Failure";
  }

  postMessage( craft_slaveMaster_msg('log', logMsg) );
  //console.log(crafted_msg);
  return crafted_msg;
};


/*!
 * @brief Crafts response message on Platform Failure
 */
function craft_error_response()
{
  var errorMsg = 'RAPP Platform Failure';
  var crafted_msg = {found_names: [], found_centers: [], found_scores: [],
    error: errorMsg};

  var logMsg = 'Return to client with error --> ' + errorMsg;
  postMessage( craft_slaveMaster_msg('log', logMsg) );
  //console.log(crafted_msg);
  return crafted_msg;
}


/*!
 * @brief Crafts ready to send, rosbridge message.
 *   Can be used by any service!!!!
 */
function craft_rosbridge_msg(args, service_name, id){

  var rosbrige_msg = {
    'op': 'call_service',
    'service': service_name,
    'args': args,
    'id': id
  };

  return rosbrige_msg;
}


function register_master_interface()
{
  // Register onexit callback function
  onexit = function(e){
    console.log("Service [%s] exiting...", __hopServiceName);
    var logMsg = "Received termination command. Exiting.";
    postMessage( craft_slaveMaster_msg('log', logMsg) );
  }

  // Register onmessage callback function
  onmessage = function(msg){
    if (__DEBUG__)
    {
      console.log("Service [%s] received message from master process",
        __hopServiceName);
      console.log("Msg -->", msg.data);
    };

    var logMsg = 'Received message from master process --> [' +
      msg.data + ']';
    postMessage( craft_slaveMaster_msg('log', logMsg) );

    exec_master_command(msg.data);
  }

  // On initialization inform master and append to log file
  var logMsg = "Initiated worker";
  postMessage( craft_slaveMaster_msg('log', logMsg) );
}


function exec_master_command(msg)
{
  var cmd = msg.cmdId;
  var data = msg.data;
  switch (cmd)
  {
    case 2055:  // Set worker ID
      __hopServiceId = data;
      break;
    case 2050:
      __masterId = data;
      break;
    case 2065:
      __cacheDir = data;
      break;
    default:
      break;
  }
}


function craft_slaveMaster_msg(msgId, msg)
{
  var msg = {
    name: __hopServiceName,
    id:   __hopServiceId,
    msgId: msgId,
    data: msg
  }
  return msg;
}
