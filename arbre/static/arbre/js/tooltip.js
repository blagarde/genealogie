"use strict";


var tooltip_div = d3.select("div.tooltip");

var tooltip = {
    draw: function(d){
        if(d.type !== "couple"){
            //sets tooltip.  t_text = content in html
            let t_text = "<strong>" + d.first_name + "</strong>";
            let dates = _makeDates(d);
            t_text += (dates === undefined) ? "" : "<br/>" + dates
            tooltip_div.html(t_text);
            return tooltip_div.style("visibility", "visible");
        }
    },
    mousemove: function(){
        return tooltip_div.style("top", (event.pageY-10)+"px")
                      .style("left",(event.pageX+10)+"px");
    },
    mouseout: function(){
        return tooltip_div.style("visibility", "hidden");
    }
}

function _makeDates(d){
    // Return a string representing a [birth..death] date range.
    // If neither date is known, return `undefined`.
    let birth_date = _getDate(d.birth_date, d.birth_date_is_approximative),
        death_date = _getDate(d.death_date, d.death_date_is_approximative);
    if (birth_date || death_date)
        if (!death_date)
            return birth_date
        else
            return [birth_date, death_date].join(" - ");
}


function _getDate(date_str, is_approximative){
    if (date_str === null)
        return ""
    let date = new Date(date_str);
    if (is_approximative)
        return "~" + date.getFullYear();
    return date.toLocaleDateString('fr-FR');
}
export default tooltip;
