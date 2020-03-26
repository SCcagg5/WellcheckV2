<?php
$message = "| " . htmlspecialchars($_POST["email"]) . " | " . htmlspecialchars($_POST["message"]) . " |";
$fp = fopen('/result/contact.txt', 'a+');
fwrite($fp, str_replace("\n","",$message) ."\n");
fclose($fp);
?>
