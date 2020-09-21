# coding: utf-8

import frida, sys

jscode = """
Java.perform(function () {
    var class_u = Java.use("com.fengnanwlkj.gongxiangApp.util.AesEcbUtils");
    class_u.decrypt.implementation = function (list1) {
        console.log("Success");
        console.log("list1:", list1);
        var result = this.decrypt(list1);
        console.log(result);
        return result;
    };
});
"""


def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


process = frida.get_usb_device().attach('com.fengnanwlkj.gongxiangApp')
script = process.create_script(jscode)
script.on('message', on_message)
print('[*] Running CTF')

script.load()
sys.stdin.read()
