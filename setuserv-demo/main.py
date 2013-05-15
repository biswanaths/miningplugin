#
#  	Date May 15, 2013
#	Author : Biswanath
#

import webapp2
import json

from google.appengine.ext import ndb

class ProblemDomain(ndb.Model):

	name = ndb.TextProperty()
	url = ndb.TextProperty()
	
	def toJson(self):
		this = {}
		this["id"]		= self.key.id()
		this["name"] 	= self.name
		this["url"] 	= self.url
		return json.dumps(this)
		
class Field(ndb.Model):
	name = ndb.TextProperty()
	
	def toJson(self):
		this = {} 
		this["id"] 		= self.key.id()
		this["name"]	= self.name
		return json.dumps(this)

class ProblemDomainHandler(webapp2.RequestHandler):

	def get(self,problemdomain_id):
		self.response.headers['Content-Type'] = 'application/json'
		problemdomain_key = ndb.Key('ProblemDomain', int(problemdomain_id))
		problemdomain = problemdomain_key.get()
		self.response.out.write(problemdomain.toJson())
		
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		newproblemdomain = json.loads(self.request.body)
		problemdomain = ProblemDomain()
		problemdomain.name = newproblemdomain["name"]
		problemdomain.url = newproblemdomain["url"]
		problemdomain_key = problemdomain.put()
		self.response.out.write(problemdomain_key.get().toJson())
		
class FieldHandler(webapp2.RequestHandler):

	def get(self,problemdomain_id,field_id):
		self.response.headers['Content-Type'] = 'application/json'
		problemdomain_key = ndb.Key('ProblemDomain', int(problemdomain_id))
		field_key = ndb.Key('Field',int(field_id))
		field = Field.get_by_id(field_key.id(),parent=problemdomain_key)
		self.response.out.write(field.toJson())
		
	def post(self):
		self.response.headers['Content-Type'] = 'application/json'
		newfield = json.loads(self.request.body)
		problemdomain_key = ndb.Key('ProblemDomain',int(newfield["problemdomain_id"]))
		field = Field(parent=problemdomain_key)
		field.name = newfield["name"]
		field_key = field.put()
		self.response.out.write(field_key.get().toJson())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
		
class PluginHandler(webapp2.RequestHandler):
	def get(self,problemdomain_id):
		self.response.headers['Content-Type'] = 'application/json'
		problemdomain_key = ndb.Key('ProblemDomain', int(problemdomain_id))
		query = Field.query(ancestor=problemdomain_key)
		fields = query.fetch()
		for field in fields:
			self.response.out.write(field.toJson())
		
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainHandler,name='home'),
	webapp2.Route(r'/plugin/<problemdomain_id:\d+>',PluginHandler,name='plugin'),
	webapp2.Route(r'/problemdomain/<problemdomain_id:\d+>',ProblemDomainHandler,name='problemdomain'),
	webapp2.Route(r'/problemdomain/save',ProblemDomainHandler,name='problemdomain'),
	webapp2.Route(r'/problemdomain/field/save',FieldHandler,name='field'),
	webapp2.Route(r'/problemdomain/<problemdomain_id:\d+>/field/<field_id:\d+>',FieldHandler,name='field'),
], debug=True)
