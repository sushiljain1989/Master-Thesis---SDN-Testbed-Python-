<?php
$old = getcwd();
chdir('/var/www/html/testbed/run_apps/');
$output = shell_exec('./test_bash.sh');
chdir($old);
echo "<pre>$output</pre>";


?>
