<!DOCTYPE html>
<html lang="en">

<head>
    <!-- FONTS -->
    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
    <!-- FAVICON -->
    <link rel="icon" type="img/ico" href="/images/logoBlackFilled.png">
    <title>Art of a Magic Pineapple</title>
    <!-- CSS -->
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/bottom.css">
    <link rel="stylesheet" href="/css/top.css">
    <link rel="stylesheet" href="/css/queries.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.6.1/css/bulma.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- JS-->
    <script src="/js/script.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#menuButtonPicDiv').click(function() {
                $('#menu').css('display', 'block');
            });
        });
    </script>
</head>

<body>
    <!-- SET BACKGROUNDS. COLORS IN MAIN.CSS -->
    <?php

    //SET PAGE HEIGHTS
    if (isset($index) || $index || $contact) {
        echo
            '<style type = "text/css">
                               
                                section{
                                        min-height: 100vh;
                                }
                                
                                #footer{
                                        height: auto !important;
                                        min-height: 0px;
                                }
                        </style>';
    }
    ?>
    <!--TOP MENU-->
    <div id="menuBar">
        <div id="menuBarContent">
            <div id="menuLogoDiv"><img id="menuLogo" src="images/pineapple.png">
            </div>
            <h1 id="menuTitle">art of a magic pineapple</h1>
            <div id="mobileMenuButtonDiv"> <img id="mobileMenuButton" src="images/menuButton.png" onclick="openMenu()"> </div>
            <div id="menuButtonBar">

                <div class="menuButtonDiv">
                    <a href="/index.php">
                        <p class="menuButtonText">art</p>
                    </a>
                </div>

                <div class="menuButtonDiv">
                    <a href="/about.php">
                        <p class="menuButtonText">about</p>
                    </a>
                </div>

                <div class="menuButtonDiv">
                    <a href="/prints.php">
                        <p class="menuButtonText">prints</p>
                    </a>
                </div>

                <div class="menuButtonDiv">
                    <a href="/life.php">
                        <p class="menuButtonText">life</p>
                    </a>
                </div>

                <div class="menuButtonDiv">
                    <a href="https://society6.com/magicpineappleart" target="_blank" rel="noopener">
                        <p class="menuButtonText">shop</p>
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- MOBILE MENU -->
    <div id="mobileMenu">
        <div id="mobileMenuContent">
            <div id="mobileExitButtonDiv"> <img onclick="closeMenu()" id="mobileExitButton" src="images/exitButton.png"> </div>
            <div id = "mobileMenuCol">
                <div class="mobileMenuButtonDiv"> <a href="/index.php">
                        <h1 class="mobileMenuButtonText"">art</h1>
                    </a> </div>
                <div class="mobileMenuButtonDiv"> <a href="/about.php">
                        <h1 class="mobileMenuButtonText"">about</h1>
                    </a> </div>
                    <div class="mobileMenuButtonDiv"> <a href="/prints.php">
                        <h1 class="mobileMenuButtonText"">prints</h1>
                    </a> </div>
                <div class="mobileMenuButtonDiv"> <a href="/life.php">
                        <h1 class="mobileMenuButtonText"">life</h1>
                    </a> </div>
                <div class="mobileMenuButtonDiv"> <a href="https://society6.com/magicpineappleart" target="_blank" rel="noopener">
                        <h1 class="mobileMenuButtonText"">shop</h1>
                    </a>
                </div>
            </div>
        </div>
    </div>