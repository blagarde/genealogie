"use strict";


function getCoordConverter(cx, cy) {
    // Returns a function that converts absolute cartesian coordinates
    // to polar coordinates centered around (cx, cy).
    // Note: Remember that the web page's Y axis is upside down.
    function cartesian2Polar(x, y){
        let relative_x = x - cx,
            relative_y = y - cy;  // Page top is y === 0.

        let distance = Math.sqrt(relative_x ** 2 + relative_y ** 2)
        let radians = Math.atan2(relative_y, relative_x) // This takes y first
        let polarCoords = { r: distance, radians: radians }
        return polarCoords;
    }

    function polar2Cartesian(distance, radians){
        let relative_x = distance * Math.cos(radians),
            relative_y = distance * Math.sin(radians);

        let x = relative_x + cx,
            y = relative_y + cy,
        	cartesianCoords = {x: x, y: y};
        return cartesianCoords;
    }
    return {
        toPolar: cartesian2Polar,
        toCartesian: polar2Cartesian
    };
}

export default getCoordConverter;