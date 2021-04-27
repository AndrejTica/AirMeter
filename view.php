       
<?php
// php code can not be viewed on website so you use echo
// php can print html syntax into "file" via echo
echo '<p></p><a href="index.html">Go back to Main Page</a><p></p>';

echo '<div class="checkbox-container">';

/*
isset(<request>) checks if value in request is set.
Checks if input type "submit" is set (Button on website pressed).
If it is not set, then ifcase is true and you can navigate further.
*/
if (!isset($_POST['submit']))
{
    //Value 'dir' in post-request is the new dir.
    //Value dir is the folder that you select
    $dir = $_POST['dir'];
   
    //first time executeing the page 'dir' in post-request is not set,
    //so it gets set now to the folder that includes .csv files
    if (!isset($dir)) $dir = 'Daten/';

    //opens directory as a directory file
    if ($dp = opendir($dir))
    {
        //Arrays get declared
        $files = array();
        $subdirs = array(); 

        //reads directory contents one by one -> while and stores them in $content
        while (($content = readdir($dp)) !== false) 
        {
             //stores files in files and dirs in dirs
            if (!is_dir($dir . $content))
            {
                $files[] = $content;
            }
            else
            {
                $subdirs[] = $content;
            }
        }
        //closing directory
        closedir($dp); 
    }
    else
    {
        // error handling
        exit('Directory not opened.'); 
    }
    //if there are subdirs they are listed as buttons
    if ($subdirs) 
    {
        //only with <form> tag you can execute get- or post-requests with you need for the buttons
        echo '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">'; 
        foreach ($subdirs as $d)
        {
            //On linux there are ".." and "." dirs, which point onto the parent directory and the current directory.
            //We do not want the user to see them.
            if ($d == ".." || $d == ".") 
            {
                continue;
            }
            //$d is name of directory an is shown on button 
            //value of button is the 'dir' (name="dir") in post-request needs to be set for next iterations
            echo '<button type="submit" name="dir" value="' . $dir . $d . '/" />' . $d . '</button>' . '<p></p>';
            

        }
        echo '</form>';
    }
    //if there are files they are listed as checkboxes
    if ($files) 
    {
        echo '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">';
        foreach ($files as $file)
        {

            echo '
                <input name="files[]" value="' . $dir . $file . '" class="inp-cbx" id="' . $file . '" type="checkbox"/>
                <label class="cbx" for="' . $file . '">
                    <span>
                        <svg width="12px" height="10px">
                            <use xlink:href="#check"></use>
                        </svg>
                    </span>
                    <span>
                        ' . $file . '
                    </span>
                </label>
                <svg class="inline-svg">
                    <symbol id="check" viewbox="0 0 12 10">
                        <polyline points="1.5 6 4.5 9 10.5 1"></polyline>
                    </symbol>
                </svg> <p></p>
            ';
        }
        echo '<p></<p><input type="submit" name="submit" value="submit" />' . '</form>';
        //variable files[] in post-request is set with the files of all ticked checkboxes
    }
}
else
{
     // if files in post-requests is set
    if (isset($_POST['files']))
    {
        // loop through all files
        foreach ($_POST['files'] as $value) 
        {
            //writing file contents into a variable
            //if unable to open -> "Unable to open file!"
            $myfile = fopen($value, "r") or die("Unable to open file!"); 
             //go through file-contents char by char until char is end of file char
            while (!feof($myfile))
            {
                 // write into csv_data which will be used for drawgraph() function
                $csv_data .= fgets($myfile);
               
            }
            //close file
            fclose($myfile);
            echo '<pre id="csv" style="display:none">'.$csv_data.'</pre>';
        }
    }
    else
    {
        exit('No files selected');
    }

    echo '</div>';

}


?> 



<!DOCTYPE html> <!-- Write your comments here -->
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Graph</title>
        <link rel="stylesheet" href="./viewPage.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prefixfree/1.0.7/prefixfree.min.js"></script>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="highcharts.js"></script>
        <script src="data.js"></script>
        <script src="exporting.js"></script>
        <script src="export-data.js"></script>
        <script src="accessibility.js"></script>
        <script src="jquery-3.5.1.min.js"></script>
        <script src="papaparse.js"></script>
        <script src="script.js"></script>
    </head>
    <body>
        <div class="BackButton">    
        </div>
        <!-- Containers for the two charts -->
        <div id="container1"></div>


<script type="text/javascript">
//function to draw charts. 
//gets the converted php var data as parameter
function drawChart() {

    //this will hold the date as title of thr chart
    let newTitle;

    let chart = Highcharts.chart('container1', {

        chart: {
            zoomType: 'x',
            events: {
                load: function () {
                    this.update({
                        title: {
                            text: 'AirMeter: ' + newTitle 
                        }
                    })
                }

            }

        },

        xAxis: {

            title: {
                text: 'Zeit'
            }
        },

        yAxis: {

            title: {
                text: 'CO2 in ppm'
            }

        },

        exporting: {
            enabled: true
        },


        title: {
            text: null 
        },

        credits: {
            enabled: false
        },

        data: {
           
            csv: document.getElementById('csv').innerHTML,
            parsed(e) {
                newTitle = new Date(e[0][5]).toDateString();  //set the first column as title of the chart

                e.shift()

            },
            complete: function(options){
              //options.series.splice(0,1)
            }
        }


    });
    
}

drawChart();
</script>

</body>
</html>
