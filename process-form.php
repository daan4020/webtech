<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $name = $_POST['name'];
  $email = $_POST['email'];
  $message = $_POST['message'];
  $to = 'Daan.devriespeize@gmail.com';
  $subject = 'Nieuw contactformulierbericht van ' . $name;
  $headers = 'From: ' . $name . ' <' . $email . '>' . "\r\n" . 'Reply-To: ' . $email;
  mail($to, $subject, $message, $headers);
  header('Location: bedankt.html');
  exit;
}
?>

