from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/get_classifier_result/<version>", methods=['GET', 'POST'])
def return_classifier_result(version):
    #TODO прочитать из полученного запроса json-контент
    #В случае, если version==1, то должен вернуться json с версией и полем predict из входящего jsonа {"version":1, "predict":<predict_value>}
    #В случае, если version==0, то должен вернуться json с версией и полем old_predict из входящего jsonа {"version":0, "predict":<old_predict_value>}
    to_return = {'version': int(version)}
    if request.method == 'POST':
        req = request.json
        if version == '1':
            to_return['predict'] = req['predict']
        if version == '0':
            to_return['predict'] = req['old_predict']
    return jsonify(to_return)

@app.route("/")
def hello():
    #TODO должна возвращатьс инструкция по работе с сервером
    return render_template('instruction.html') # лежит в templates

if __name__ == "__main__":
    app.run()
