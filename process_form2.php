<?php
  if ($_SERVER["REQUEST_METHOD"] == "POST") {
     
        $name = $_POST["name"];
        $gender = $_POST["gender"];
        $subscribe = isset($_POST["subscribe"]) ? "Yes" : "No";
        $country = $_POST["country"];

       echo "<p>Name: $name</p>";
        echo "<p>Gender: $gender</p>";
        echo "<p>Subscribe to newsletter: $subscribe</p>";
        echo "<p>Country: $country</p>";
    } else {
        echo "<p>Form not submitted.</p>";
    }
    ?>
