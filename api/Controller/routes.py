from .routesfunc import *

def setuproute(app, call):
    @app.route('/test/',            ['OPTIONS', 'POST', 'GET'], lambda x = None: call([])                                            )
    @app.route('/login/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([getauth])                                     )
    @app.route('/signup/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signup, signin, gettoken])            )
    @app.route('/signin/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, signin, gettoken])                    )
    @app.route('/renew/',    	    ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, gettoken])                  )
    @app.route('/infos/',    	    ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, infos])                     )
    @app.route('/updateinfos/',    	['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, upinfos])                   )
    @app.route('/addcard/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, addcard])                   )
    @app.route('/delcard/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, delcard])                   )
    @app.route('/listcard/',    	['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, listcard])                  )
    @app.route('/payments/',    	['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, payments])                  )
    @app.route('/paymentdetails/',  ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, paymentdetails])            )
    @app.route('/order/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, cmd_decode, pay, ordering]) )
    @app.route('/orderdetail/',    	['OPTIONS', 'POST'],        lambda x = None: call([myauth, authuser, orderdetails])              )
    @app.route('/history/',    	    ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authuser, history])                   )
    @app.route('/emulate/',    	    ['OPTIONS', 'POST'],        lambda x = None: call([myauth, emulate])                             )
    @app.route('/adm/login/',    	['OPTIONS', 'POST'],        lambda x = None: call([myauth, admtoken])                            )
    @app.route('/adm/users/',       ['OPTIONS', 'GET'],         lambda x = None: call([myauth, authadmin, all_users])                )
    @app.route('/adm/spoof/',       ['OPTIONS', 'POST'],        lambda x = None: call([myauth, authadmin, gettokenadm])              )
    def base():
        return
