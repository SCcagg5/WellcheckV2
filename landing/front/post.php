<?php
$message = htmlspecialchars($_POST["email"]) . ' | ' . htmlspecialchars($_POST["message"]);
mail("eliot.courtel@wanadoo.fr", "Wellcheck - Contact", $message);
?>
