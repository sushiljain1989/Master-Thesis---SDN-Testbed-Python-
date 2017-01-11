<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');
//session_start();
 $worker= new GearmanWorker();
$worker->addServer();
$worker->addFunction("reverse", "my_reverse_function");
while (1){
	$worker->work();
}

function my_reverse_function($job)
{

	$link = mysqli_connect("localhost", "root", "sunset", "jobs");
	
	while(1){
			if ($result = mysqli_query($link, "select * from jobs where status = 'Pending'")) {

		    /* determine number of rows result set */
		    $row_cnt = mysqli_num_rows($result);

		   if($row_cnt > 0)
		   {
		   		while($row = mysqli_fetch_array($result,MYSQLI_ASSOC))
		   		{
		   			$query = "update jobs set status = 'Processing' where id = ". $row['id'];
		   			mysqli_query($link , $query);
		   			sleep(1);
		   			
		   			$old = getcwd();
					chdir('/home/vagrant/');
					#echo './testbed4.sh -a 1 -c'.$row['controller'].' -m t';
					$output = shell_exec('./testbed4.sh -a '.$row['name']. ' -c '.$row['controller'].' -m t');
					chdir($old);
					#echo "<pre>$output</pre>";
					$file = "/home/vagrant/testbed/logs/mininet_".$row['controller']."_".$row['name'].".out";
		   			$handle = fopen($file, "r");
		   			$data = array();
					if ($handle) {
					    while (($line = fgets($handle)) !== false) {
					        // process the line read.
					        array_push($data, $line);
					    }

					    fclose($handle);
					} else {
					    // error opening the file.
					} 
					$date = date('Y-m-d H:i:s');
		   			$query = "update jobs set finished = '".$date."', status = 'Finished', pingall = '".trim($data[0])."', flow_rules = '".trim($data[1])."' where id = ". $row['id'];
		   			mysqli_query($link , $query);
		   		}
		   }

		    /* close result set */
		    mysqli_free_result($result);
		   

			}
			sleep(5);
	}
	mysqli_close($link);
	/*$status = "Pending";
	$stmt = $mysqli->prepare("select * FROM jobs");
	//$stmt->bind_param("s", $status);
	$stmt->execute();
	$result = $stmt->get_result();
	echo $stmt->num_rows;
	if($stmt->num_rows > 0)
	{
		while($row = $stmt->fetch_assoc())
		{
			echo "<pre>"; print_r($row); "</pre>";
		}
	}
	$stmt->close();

	$mysqli->close();*/


	/*session_id($job->workload());
	//session_start();
	#print_r($_SESSION);die;
	/*print_r($_SESSION);

	print "hello";
	
	sleep(2);
	print "hello";
	sleep(2);
	print "hello";
	sleep(2);
	print "hello";
	print "hello";
	sleep(2);
	print "hello";
	sleep(2);
	print "hello";
	sleep(2);
	foreach($_SESSION as $k => $v)
  	{
  		foreach ($v as $key => $value) {
  			//echo "executing ($k) : " . $key;
  			sleep(2);
  			$_SESSION[$k][$key] = "Running";
  			sleep(3);
  			$_SESSION[$k][$key] = "Finished";
  		}
  	}
  	return;*/
  //return strrev($job->workload());
}
?>
