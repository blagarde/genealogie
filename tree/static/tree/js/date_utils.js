"use strict";


var getDateUtils = function(data, reverse=false){
    // Map the range of birth dates [earliest..latest] to the interval [0..1].
    // Return a function that converts a date string to a float by scaling.
    const birth_dates = data.nodes.map((p) => p.birth_date)
                                    .filter(Boolean)
                                    .map(p => new Date(p)),
        earliest_date = new Date(Math.min(...birth_dates)),
        latest_date = new Date(Math.max(...birth_dates)),
        range = (latest_date - earliest_date);

    var self = {
        start: earliest_date,
        end: latest_date,
        range: range,
        reverse: reverse
    }

    self.converter = function(date_str){
        let date = new Date(date_str);
        return (self.reverse ? (latest_date - date) : (date - earliest_date)) / range
    }

    self.getTicks = function(interval_years){
        // Return a range of dates normalized as floats against the interval [earliest..latest].
        // The dates are like YYYY-01-01, separated by `interval_years` intervals.
        // They start before `earliest_date` and end after `latest_date`.
        const start = Math.floor(earliest_date.getFullYear() / interval_years) * interval_years;
        const end = Math.ceil(latest_date.getFullYear() / interval_years) * interval_years;
        const n_steps = (end - start) / interval_years;
        return [...Array(n_steps + 1).keys()].map(function(i){
            let year = start + interval_years * i,
                date_str = year + "-01-01",
                value = self.converter(date_str);
            return {year: year, value: value}
        });
    }

    return self;
}

export default getDateUtils;
