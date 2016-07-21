<?php
    $output = `/usr/bin/python /var/www/ping_map/host.py`;
    //    $output = `/bin/cat /var/www/ping_map/host_status.txt`;

    echo json_decode($output);
?>
