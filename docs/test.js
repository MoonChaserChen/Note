function stringifyObj(t) {
    if (t === null) {
        return t;
    }
    //数组
    if (Array.isArray(t)) {
        const list = [...t].sort().reduce((acc, item) => {
            if (typeof item === 'object') {
                acc.push(sortObj(item));
            } else {
                acc += item;
            }
            return acc;
        }, []);
        return JSON.stringify(list);
    }
    // 是对象非数据
    if (typeof t === 'object') {
        return Object.keys(t)
            .sort()
            .reduce((acc, key) => {
                if (typeof t[key] === 'object') {
                    return (acc += `${key}=${JSON.stringify(sortObj(t[key]))}&`);
                }
                    return (acc += `${key}=${t[key]}&`);
            }, '');
    }
}

function sortObj(obj) {
    if (obj === null) {
        return obj;
    }
    if (Array.isArray(obj)) {
        return [...obj].sort().reduce((acc, item) => {
            if (typeof item === 'object') {
                acc.push(sortObj(item));
            } else {
                acc.push(item);
            }
            return acc;
        }, []);
    }
    if (typeof obj === 'object') {
        return Object.keys(bj)
            .sort()
            .reduce((acc, key) => {
                if (typeof obj[key] === 'object') {
                    acc[key] = sortObj(obj[key]);
                } else {
                    acc[key] = obj[key];
                }
                return acc;
            }, {})
    }
}

function getParameter() {
    let parameter = null
    if (request.method === 'GET') {
        var toType = function(a) {
            return ({}).toString.call(a).match(/\s([a-zA-Z]+)/)[1].toLowerCase();
        }, map = {};

        // http://localhost:8080/newYearActivity/helloUser?a=1
        var params = request.url.split("?")
        if (params.length < 2) {
            return {}
        }
        // (.+\?)=?([^&]*)(?:&+|$)
        params[1].replace(/([^&|\?=]+)=?([^&]*)(?:&+|$)/g, function (match, key, value) {
            if (key in map) {
                if (toType(map[key]) !== 'array') {
                    map[key] = [map[key]];
                }
                map[key].push(value);
            } else {
                map[key] = value;
            }
        });
        return map;
    }

    if (request.method === 'POST') {
        parameter = JSON.parse(request.data)
    }
    return parameter
}

const SECRET = '8k&^$Hsk1?kkcj12^99K1ia'
const timestamp = +new Date()
const parameter = getParameter()
const nonce = Math.round(Math.random()*1000)
const signString = stringifyObj({...parameter, timestamp, nonce}) + SECRET
const sign = CryptoJS.SHA256(signString).toString()

request.headers.timestamp = timestamp
request.headers.sign = sign
request.headers.nonce = nonce

Object.keys(request.headers).forEach(key => {
    postman.__execution.request.headers.members.push({key:key, value:request.headers[key]});
})
