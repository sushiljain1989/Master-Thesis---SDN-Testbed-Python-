<?php

		$client= new GearmanClient();
		$client->addServer();
		$data = session_id();
		$jobHandle =  $client->doBackground("reverse" , "start_test_bed");


?>