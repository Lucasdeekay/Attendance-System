
function calculate(a, b, textSuccess, textDanger, id) {
  var val1 = parseInt(a);
  var val2 = parseInt(b);

  var svgId = document.getElementById(id)

  var total = val1+val2;

  var per1 = Math.round(val1/total*100);
  var per2 = Math.round(val2/total*100);
  var offset = 25;

  var style = "stroke-dasharray 0.5s ease-in-out, stroke-dashoffset 0.5s ease-in-out";


   svgId.innerHTML += ` <!--  GREEN  -->
                                <circle class="donut-segment2" cx="21" cy="21" r="15.91549430918954" fill="transparent"
                                        stroke="green" stroke-width="3" stroke-dasharray="${ per1+' '+(100-per1) }"
                                        style="transition: ${ style }"
                                        stroke-dashoffset="${ offset }"></circle>

                                <!--  RED  -->
                                <circle class="donut-segment1" cx="21" cy="21" r="15.91549430918954" fill="transparent"
                                        stroke="red" stroke-width="3" stroke-dasharray="${ per2+' '+(100-per2) }"
                                        style="transition: ${ style }"
                                        stroke-dashoffset="${ 100-per1+offset }"></circle>

                                <g class="chart-text">
                                    <rect x="55%" y="11%" width="2" height="2"
                                        style="fill:green" />
                                    <text x="75%" y="20%" fill="green" class="chart-number">
                                        ${ textSuccess } - ${ per1 }%
                                    </text>
                                    <rect x="55%" y="32%" width="2" height="2"
                                        style="fill:red" />
                                    <text x="78%" y="40%" fill="red" class="chart-number">
                                        ${ textDanger } - ${ per2 }%
                                    </text>
                                </g>`;
}

// line positioning: (100 - previous percent(s) + offset (25% in the opposite direction from 3:00 back to 12:00 to correct pie position)