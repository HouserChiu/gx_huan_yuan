# -*- coding: utf-8 -*-

import frida

def on_message(message, data):
    if message['type'] == 'send':
        print(message['payload'])
    elif message['type'] == 'error':
        print(message['stack'])


source = '''
rpc.exports = {
    getsig: function () {
        var ciphertext = "";
        Java.perform(function () {
            var MainActivity = Java.use('okio.Buffer');
            ciphertext = MainActivity.md5()
        })
        return ciphertext
    }
};
'''

session = frida.get_usb_device().attach('com.fengnanwlkj.gongxiangApp')
script = session.create_script(source)
script.on('message', on_message)
script.load()
print(script.exports.getsig())
session.detach()