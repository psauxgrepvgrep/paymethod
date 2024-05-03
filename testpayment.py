#!/usr/bin/python3

import payment
import sys
import tinkoff_api
import billmgr.logger as logging

MODULE = 'payment'
logging.init_logging('testpayment')
logger = logging.get_logger('testpayment')

class TestPaymentCgi(payment.PaymentCgi):
    def Process(self):
        # необходимые данные достаем из self.payment_params, self.paymethod_params, self.user_params
        # здесь для примера выводим параметры метода оплаты (self.paymethod_params) и платежа (self.payment_params) в лог
        logger.info(f"paymethod_params = {self.paymethod_params}")
        logger.info(f"payment_params = {self.payment_params}")

        terminalkey = self.paymethod_params["terminalkey"]
        terminalpsw = self.paymethod_params["terminalpsw"]

        # get float rubbles, transform 2 int
        amount_f = self.payment_params["paymethodamount"]
        amount = int(amount_f * 100)

        request_result = tinkoffapi.init_standard(terminalkey, terminalpsw, amount, self.elid, "Оплата Test", self.success_page, self.fail_page)

        # переводим платеж в статус оплачивается
        if request_result.success:
            payment.set_in_pay(self.elid, request_result.to_json(), request_result.payment_id)
        else:
            payment.set_canceled(self.elid, request_result.to_json(), "")

        # url для перенаправления c cgi
        # здесь, в тестовом примере сразу перенаправляем на страницу BILLmanager
        # должны перенаправлять на страницу платежной системы
        redirect_url = request_result.paymentURL if request_result.success else self.fail_page

        # формируем html и отправляем в stdout
        # таким образом переходим на redirect_url
        payment_form =  "<html>\n";
        payment_form += "<head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>\n"
        payment_form += "<link rel='shortcut icon' href='billmgr.ico' type='image/x-icon' />"
        payment_form += "	<script language='JavaScript'>\n"
        payment_form += "		function DoSubmit() {\n"
        payment_form += "			window.location.assign('" + redirect_url + "');\n"
        payment_form += "		}\n"
        payment_form += "	</script>\n"
        payment_form += "</head>\n"
        payment_form += "<body onload='DoSubmit()'>\n"
        payment_form += "</body>\n"
        payment_form += "</html>\n";

        sys.stdout.write(payment_form)


TestPaymentCgi().Process()
