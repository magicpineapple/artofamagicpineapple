</div>
</div>
</main>
<!--SET FOOTER POSITION ACCORDING TO PAGE-->
<?php
if (isset($index) || $contact) {
    echo
        '<style type="text/css">
                            .footer{
                                    top: 100%;
                            }
                        </style>';
} else {
    echo
        '<style type="text/css">
                            .footer{
                                    top: auto;
                            }
                        </style>';
}
?>
<div id="footerBar">
    <div id="footerBarContent">
        <div id="footerCopyright">
            <p class="footerText">@ 2019 Art of a Pineapple. All rights reserved.</p>
        </div>

        <div id="footerSocialBar">
            <a class="socialMedia" href="https://artofamagicpineapple.tumblr.com/" target="_blank" rel="noopener">
                <i class="fa fa-tumblr"></i>
            </a>
        </div>

    </div>
</div>
</body>

</html>