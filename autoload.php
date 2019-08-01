<?php

spl_autoload_register(function ($class) {
    require __DIR__ . '/' . $class . '.php';
});

//require __DIR__ . '/data/constants.php';
