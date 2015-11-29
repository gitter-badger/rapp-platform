/*!
 * @file fileUtils.js.js
 * @brief Functionalities on working with files. Read, Write, Remove, Path..
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


var fs = require('fs');
var path = require('path');


/*!
 * @brief Resolve input path to absolute path.
 * @param _path Path to be resolved to absolute.
 * @return Resolved absolute path.
 */
function resolvePath( _path )
{
  var regexp = /~/g;
  var newPath = '';
  if ( _path.match( regexp ) )
  {
    var user = process.env.LOGNAME;
    /*<Replaces "~" with "/home/user">*/
    newPath = _path.replace( regexp, '/home/' + user );
  }
  else
  {
    newPath = path.resolve( _path );
  }
  return newPath;
};


/*!
 * @brief Wrapping Node.js readFileSync function.
 * @param _file File to be read, specified by path.
 * @param _encoding Encoding type of returned data
 *  readen from the specified file. Can be one of the following:
 *  1) "buffer" OR undefined Raw data from buffer.
 *  2) "string/ascii" Ascii encoded string.
 *  3) "string/binary" Binary encoded string.??
 *  4) "string/utf8" Utf8 encoded string. Currently not working with HOP!!
 *
 * @return Returns data readen from file.
 */
function readFileSync( _fileUrl, _encoding )
{
  var file = {
    data: undefined,
    encoding: undefined,
    basename: undefined,
    absolutePath: undefined,
    size: {
      bytes: undefined,
      kilobytes: undefined,
    }
  }
  var fileAbsPath = resolvePath( _fileUrl );
  if( fs.existsSync( fileAbsPath ) )
  {
    file.absolutePath = fileAbsPath;
    file.basename = path.basename( fileAbsPath );
    var dataBuffer = fs.readFileSync( fileAbsPath );
    file.size['bytes'] = dataBuffer.length;
    file.size['kilobytes'] = file.size['bytes'] / 1024;
    console.log("\033[0;33mReading requested file:" +
      "[%s] , filesize: [%s]\033[0;0m", fileAbsPath, file.size['bytes']);
    encoding = _encoding || "none";
    switch ( encoding )
    {
      case "buffer":
        file.data = dataBuffer;
        file.encoding = "raw";
        break;
      case "ascii":
        var str = dataBuffer.toString( 'ascii' );
        file.data = str;
        file.encoding = "ascii";
        break;
      case "string/utf8":
        var str = dataBuffer.toString( 'utf8' );
        file.data = str;
        file.encoding = "utf8";
        break;
      case "string/binary":
        var str = dataBuffer.toString( 'binary' );
        file.data = str;
        file.encoding = "binary";
        break;
      case "none":
        file.data = dataBuffer;
        file.encoding = "raw";
        break;
      default:
        console.log( '\033[0;31mGiven encoding is not supported\033[0;0m' );
    }
    return file;
  }
  else
  {
    console.log("\033[01;31mCannot access the requested file. File does not exist.\033[0;0m");
    return 0;
  }
};


/*!
 * @brief Wrapping Node.js writeFileSync function
 * @param _dest Destination file name to write the data, specified by path.
 * @param _data Data to be written.
 * @return Undefined.
 */
function writeFileSync( _destUrl, _data )
{
  var path =  resolvePath( _destUrl );
  if( fs.existsSync( path ) ){
    console.log("\033[0;36mFile [%s] allready exists. Overwriting...\033[0;0m", path);
  }
  else{
    //console.log("\033[0;36mWriting requested data @ [%s]\033[0;0m", path);
  }

  try{
    fs.writeFileSync( path, _data );
  }
  catch(e){
    // TODO !!!!
    return false;
  }

  var filesize = fileSize( path );
  //console.log("\033[0;36mFinished writing requested data" +
    //"@ [%s] , filesize: [%s]\033[0;0m", path, filesize);
  return true;
};


/*!
 * @brief Creates directory non-recursively
 */
function createDir(dirPath)
{
  var dir = resolvePath(dirPath);
  if ( fs.existsSync(dir) ) { return true; }

  try{
    fs.mkdirSync(dir);
  }
  catch(e){
    return false;
  }

  return true;
}


/*!
 * @brief Creates directory recursively --> a/b/c/d
 */
function createDirRecur(dirPath)
{
  dirPath = resolvePath(dirPath);
  if ( fs.existsSync(dirPath) ) { return true; }
  if( createDir(dirPath) == false )
  {
    // Create all the parents recursively
    createDirRecur(path.dirname(dirPath));

    // Then create the child directory
    createDirRecur(dirPath);
  }
}


/*!
 * @brief Wrapping Node.js unlinkSync function.
 * @param _file File to be removed, specified by path.
 * @return True if file existed and removed, false otherwise.
 */
function rmFile(_file)
{
  var filePath =  resolvePath(_file);
  if( fs.existsSync(filePath) && isFile(filePath) )
  {
    fs.unlinkSync(filePath);
    //console.log("Successfully deleted file: [%s]", path);
    return true;
  }
  else
  {
    //console.log("\033[0;31mFile [%s] does not exist!\033[0;0m", path);
    return false;
  }
};


/*!
 * @brief Reads the contents of a given directory path.
 * @param _dir Directory path. Works both with relative and absolute paths.
 * @return List of the contents of the specific directory (Array).
 */
function lsSync( _dir )
{
  var fileList = [];
  var dir = resolvePath( _dir );
  var files = fs.readdirSync(dir);
  for(var i in files)
  {
    var fullPath = dir + '/' + files[i];
    if (fs.statSync(fullPath).isDirectory())
    {
      continue;
    }
    else{
      fileList.push( files[i] );
    }
  }
  return fileList;
};


/*!
 * @brief Writes ascii encoded strings in a give file.
 * @param _data Data to be written. Can be both a buffer or string.
 * @param _filePath Destination file path.
 * @return Undefined.
 * @TODO REFACTOR!!!
 */
function text2File ( _data, _filePath ){
  if ( Buffer.isBuffer( _data ) ){
    var data = _data;
  }
  else if ( typeof _data == 'string' ){
    var data = new Buffer( _data.length );
    data.write( _data );
  }
  else{
    console.log( "\033[01;31mInvalid Type of input parameter." +
      "Only String and Buffer data are valid!\033[0;0m" );
    return;
  }

  var fd = fs.openSync( _filePath, 'w' );
  var numBytes = fs.writeSync( fd, data, 0, data.length, null );
  fs.close( fd );
};


function appendLine( str, dest )
{
  var destPath = resolvePath(dest);
  fs.appendFileSync(destPath, str + '\n');
}


/*!
 * @brief Getting File Size without Reading Entire File.
 * @param _fileURL File System Url.
 * @return Size of the file in bytes.
 */
function fileSize( _fileURL ) {
  var path =  resolvePath( _fileURL );
  var stats = fs.statSync( path );
  var filesize_bytes = stats["size"];
 return filesize_bytes;
};


/*!
 * @brief Load json file
 * @param fileName.
 * @param encoding Encoding definition.
 */
function load_json_file(filename, encoding) {
  try {
    // default moduleencoding is utf8
    if (typeof (encoding) == 'undefined') encoding = 'utf8';
    // read file sync
    var contents = fs.readFileSync(filename, encoding);
    // parse contents as JSON
    return JSON.parse(contents);
    //
    }
  catch (err) {
  // an error occurred
    throw err;
  }
};


/*!
 * @brief Rename file. Can also be used as a funcitonality to copy files.
 * @param fileOld Source file path.
 * @param fileNew Destination file path.
 */
function renameFile(file, dest)
{
  var sourcePath = resolvePath(file);
  var destPath = resolvePath(dest);
  var destDir = parentDir(destPath);

  // If source file and destination file match then do not proceed.
  if (sourcePath == destPath) {return true;}

  // If parent directory of given destination file does not exist,
  // return false immediately.
  if ( destDir == false || fs.existsSync(destDir) == false ||
    (! isFile(sourcePath)) )
    {return false};

  // Check if source file exists and destination directory also exists.
  if ( fs.existsSync(sourcePath) )
  {
    try{
      fs.renameSync(sourcePath, destPath);
    }
    catch(e){
      console.error("Failed to rename file [%s] --> [%s] , ErrorCode: [%s]",
        sourcePath, destPath, e);
      return false;
    }
    return true;
  }
  else {return false;}
}


/*!
 * @brief Copies file from-To. Uses read/write streams and pipes.
 * @param file File (given with either relative or absolute path to copy
 * @param dest Destination to copy the file.
 */
function copyFile(file, dest)
{
  var sourcePath = resolvePath(file);
  var destPath = resolvePath(dest);
  var destDir = parentDir(destPath);

  // If source file and destination file match then do not proceed.
  if ( sourcePath == destPath ) {return true;}

  // If parent directory of given destination file does not exist,
  // return false immediately.
  if ( destDir == false || fs.existsSync(destDir) == false ) {return false};

  // Check if source file exists and destination directory also exists.
  if( fs.existsSync( sourcePath ) )
  {
    try{
      //fs.createReadStream(sourcePath).pipe(fs.createWriteStream(destPath));
      fs.writeFileSync(destPath, fs.readFileSync(sourcePath));
    }
    catch(e){
      console.error("Failed to copy file [%s] --> [%s] . ErrorCode: {}",
        sourcePath, destPath, e);
      return false;
    }
    return true;
  }
  else {return false;}  // If source file does not exist return false.
}


/*!
 * @brief Returns the parent directory name for given path.
 * @return The parent directory. In case of error a zero 0 value will be
 * returned.
 */
function parentDir(_path)
{
  var absPath = resolvePath(_path);
  try
  {
    var parentDir = path.dirname(absPath);
  }
  catch(e)
  {
    console.log(e);
    return false;
  }
  return parentDir;
}


function isDirectory(_path)
{
  var dirPath = resolvePath(_path);
  var isDir = false;
  if( fs.existsSync(_path) ) {isDir = fs.lstatSync(_path).isDirectory();}
  return isDir;
}


function isFile(_path)
{
  var filePath = resolvePath(_path);
  var isFile = false;
  if( fs.existsSync(_path) ) {isFile = fs.lstatSync(_path).isFile();}
  console.log(isFile)
  return isFile;
}

/**
 * This module exports.
 */
module.exports = {
  resolvePath: resolvePath,
  readFileSync: readFileSync,
  writeFileSync: writeFileSync,
  rmFile: rmFile,
  lsSync: lsSync,
  text2File: text2File,
  appendLine: appendLine,
  fileSize: fileSize,
  load_json_file: load_json_file,
  renameFile: renameFile,
  createDir: createDir,
  createDirRecur: createDirRecur,
  copyFile: copyFile,
  parentDir: parentDir,
  isDirectory: isDirectory,
  isFile: isFile
}
