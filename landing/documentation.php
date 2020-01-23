<!doctype html>
<!--
	Solution by GetTemplates.co
	URL: https://gettemplates.co
-->
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="owl-carousel/assets/owl.carousel.min.css" type="text/css">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <!-- custom CSS -->
    <link rel="stylesheet" href="css/style.css">
    <title>Wellcheck</title>
    <link rel="icon" href="imgs/logo-min.png" type="image/gipng">
    <!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-154947792-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-154947792-1');

  function changefile(file){
    document.getElementById('viewer').data = file;
    document.getElementById('link').href = file;
  }
</script>

</head>
<body class="fullscreen">
<nav class="navbar navbar-expand-lg navbar-light bg-light bg-transparent" id="gtco-main-nav">
    <div class="container"><a class="navbar-brand" href="/index">Wellcheck</a>
        <button class="navbar-toggler" data-target="#my-nav" onclick="myFunction(this)" data-toggle="collapse"><span
                class="bar1"></span> <span class="bar2"></span> <span class="bar3"></span></button>
        <div id="my-nav" class="collapse navbar-collapse">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item">
                  <select name="doc" class="nav-select" onchange="changefile(this.options[this.selectedIndex].value)">
                    <option value="pdfs\Wellcheck_012020.pdf" class="opt" selected>Presentations</option>
                    <option value="pdfs\Wellcheck_012020.pdf" class="opt">[FR] January 2020</option>
                    <option value="pdfs\Wellcheck_072019.pdf" class="opt">[ENG] July 2019</option>
                  </select>
                </li>
            </ul>
            <form class="form-inline my-2 my-lg-0">
                <a href="https://dashboard.wellcheck.fr#view=Fit" class="btn btn-outline-dark my-2 my-sm-0 mr-3 text-uppercase">Early acces</a>
            </form>
        </div>
    </div>
</nav>
<object id="viewer" data="pdfs\Wellcheck_012020.pdf" type="application/pdf" class="pdf">
  <p>Your web browser doesn't have a PDF plugin.
  Instead you can <a id='link' href="pdfs\Wellcheck_012020.pdf">click here to
  download the PDF file.</a></p>
</object>
<footer class="container-fluid" id="gtco-footer">
    <div class="container">
            <div class="col-12 text-center">
                <p>Wellcheck&copy; 2019. All Rights Reserved.</p>
            </div>
    </div>
</footer>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery-3.3.1.slim.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<!-- owl carousel js-->
<script src="owl-carousel/owl.carousel.min.js"></script>
<script src="js/main.js"></script>
</body>
</html>
