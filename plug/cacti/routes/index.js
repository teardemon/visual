var express = require('express');
var router = express.Router();
var async=require('async');
var database = require('../models/database');
var data = new database();

/* GET home page. */
router.get('/:id', function(req, res, next) {
    var id=req.params.id;
    async.parallel(
        [
            function(callback)
            {
                var temp='/var/lib/cacti/rra/'+id;
               // var sql="select graph_local.id from graph_local,poller_item where graph_local.host_id=poller_item.host_id and rrd_path='"+ temp +"'";
                var sql="select distinct graph_local.id,rrd_path from graph_local,poller_item where graph_local.host_id=poller_item.host_id and rrd_path='"+ temp +"' and snmp_query_id=1";
                data.mconnect();
                data.findMoreById(sql,function (ret){
                    callback(null,ret);
                })
                data.distroy();
            }
        ],
        function(err, results) {
            res.send(results[0]);
        }
    )

});

module.exports = router;
