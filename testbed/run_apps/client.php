<?php
error_reporting( E_ALL );
session_start();
session_destroy();die;

if(!isset($_SESSION['gearman'])){
$client= new GearmanClient();
$client->addServer();
$jobHandle =  $client->doBackground("reverse", "Hello World!");
$_SESSION['gearman'] = $jobHandle;
print_r($_SESSION);
print "hello";

}
else
{
	$client= new GearmanClient();
	$client->addServer();
	$status = $client->jobStatus($_SESSION['gearman']);
	echo "<pre>"; print_r($status); echo "</pre>";
	if (!$status[0]) // the job is known so it is not done
      $done = true;
   echo "Running: " . ($status[1] ? "true" : "false") . ", numerator: " . $status[2] . ", denomintor: " . $status[3] . "\n";
   #session_destroy();
}
?>
