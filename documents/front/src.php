<?php
  function get_pdf($id, $start, $end, $DL = 'false'){
    $curl = curl_init();
    curl_setopt_array($curl, array(
      CURLOPT_URL => "map_bck-end:8080/pdf/report/",
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_ENCODING => "",
      CURLOPT_MAXREDIRS => 10,
      CURLOPT_TIMEOUT => 0,
      CURLOPT_FOLLOWLOCATION => true,
      CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
      CURLOPT_CUSTOMREQUEST => "POST",
      CURLOPT_POSTFIELDS =>"{\"points_id\": [\"".$id."\"], \"period_start\": ".$start.", \"period_end\": ".$end."}",
      CURLOPT_HTTPHEADER => array(
        "Content-Type: application/json"
      ),
    ));
    $response = curl_exec($curl);
    curl_close($curl);
    //var_dump(json_decode($response)->data->Content);
    $file = base64_decode(json_decode($response)->data->Content);

    header('Cache-Control: public');
    header('Content-Type: application/pdf');
    header('Content-Length: '.strlen($file));
    if ($DL == 'true'){
      header('Content-Disposition: attachment; filename="report.pdf"');
    }
    print($file);
    //var_dump($response);
  }
  if (isset($_GET["id"]) &&  isset($_GET["from"]) && isset($_GET["to"])) {
    get_pdf($_GET["id"], $_GET["from"], $_GET["to"]);
  }
