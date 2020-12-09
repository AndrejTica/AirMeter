const options = {
        chart:{
           
            zoomType: 'xy'

        },

        tooltip:{
            formatter(){
                return `Zeit - ${this.x}. ppm - ${this.y}`;

            }

        },

        credits:{                   //credit aus
            enabled: false
        },

        title: {
            text: 'Airmeter'
        },
        
        xAxis:{
            title:{
                text: 'Zeit'
            },
            type:'datetime'

        },

        yAxis:{
            title:{
                text: 'CO2 in ppm'
            }

        }
    };