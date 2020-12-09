document.addEventListener('DOMContentLoaded', () =>{    //callback function
  
    const options = {
        chart:{

            zoomType: 'xy'

        },

        // tooltip:{
        //     formatter(){
        //         return `Zeit - ${this.x}. ppm - ${this.y}`;

        //     }

        // },

        credits:{                   //credit aus
            enabled: false
        },

        title: {
            text: 'Airmeter'
        },

        xAxis:{
            type: 'datetime', //funktioniert nur wenn ich monat und tag auch hab
            title:{
                text: 'Zeit'
            }
        },

        yAxis:{
          

            title:{
                text: 'CO2 in ppm'
            }

        } 
    };
       
       
     $.get('test.csv', csv => {
        options.data = {
            csv
        };
        Highcharts.chart('container', options); //highchart global variable from library 
     });

    // options.data = {
    //     csvURL: '/home/andrej/Documents/LastSchoolYear/Airmeter/website/test.csv',
    //     enablePolling: true,
    //     dataRefreshRate: 2
    // }
    // Highcharts.chart('container', options);
});

