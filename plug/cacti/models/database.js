/**
 * Created by Administrator on 2016/7/18.
 */
/**
 * Created by Administrator on 2016/5/6.
 */

var Util = require('./util')
    , mysql = require('mysql')
    , dbClient;

module.exports = function()
{
    this.findOneById = function(sql,callback){
        dbClient.query(sql,
            function(error, results) {
                if (error) {
                    console.log('GetData Error: ' + error.message);
                    dbClient.end();
                    callback(false);
                } else {
                    if(results){ //如果查询到数据则返回一条数据即可
                        callback(results.pop());
                    } else{ //查询数据为空则返回空数据
                        callback(results);
                    }
                }
            });
    };


    this.findMoreById = function(sql,callback){
        dbClient.query( sql ,
            function(error, results) {
                if (error) {
                    console.log('GetData Error: ' + error.message);
                    dbClient.end();
                    callback(false);
                } else {
                    callback(results);
                }
            });
    };

    /**
     * @desc 向数据库插入数据
     * @param tableName string
     * @param rowInfo json
     * @param callback function
     * @return null
     */
    this.insert = function(tableName, rowInfo, callback){
        dbClient.query('INSERT INTO ' + tableName + ' SET ?', rowInfo,
            function(err, result) {
                if (err) {
                    dbClient.end();
                    throw err;
                }else{
                    callback(result.insertId);
                }
            });
    };

    /**
     * @desc 修改数据库的一条数据
     * @param tableName string
     * @param idJson json
     * @param callback function
     * @return null
     */

    this.modify = function(tableName, idJson, rowInfo, callback){
        dbClient.query('update ' + tableName + ' SET ? where ?', [rowInfo, idJson],
            function(err, result) {
                if(err) {
                    console.log("ClientReady Error: " + err.message);
                    callback(false);
                    dbClient.end();
                } else {
                    callback(result);
                }
            });
    };

    /**
     * @desc 删除数据库的一条数据
     * @param tableName string
     * @param idJson json
     * @param rowInfo json
     * @param callback function
     * @return null
     */
    this.remove = function(tableName, idJson, callback){
        dbClient.query('delete from ' + tableName + ' where ?', idJson,
            function(error, results) {
                if(error) {
                    console.log("ClientReady Error: " + error.message);
                    dbClient.end();
                    callback(false);
                } else {
                    callback(true);
                }
            });
    };


    this.mconnect=function(){
        var dbConfig = Util.get('package.json', 'database');
        /* 获取mysql配置信息 */
        client = {};
        client.host = dbConfig['host'];
        client.port = dbConfig['port'];
        client.user = dbConfig['user'];
        client.password = dbConfig['password'];
        dbClient = mysql.createConnection(client);
        dbClient.connect();
        /* 执行mysql指令，连接mysql服务器的一个数据库 */
        dbClient.query('USE ' + dbConfig['dbName'], function(error, results) {
            if(error) {
                console.log('ClientConnectionReady Error: ' + error.message);
                dbClient.end();
            }
            if(!error){

            }
        });
    };


    this.distroy=function(){
        dbClient.end();
    };

};