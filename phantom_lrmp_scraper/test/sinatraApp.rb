#require 'rubygems'
require 'sinatra'
#require 'sinatra/reloader'
require 'sinatra/content_for'
require 'sinatra/partial'
require 'json'

require 'pry'

set :partial_template_engine, :erb
enable :partial_underscores
enable :sessions
#set :public_folder, File.dirname(__FILE__) + '/' #serve everything
@@test_data ||= {}

get '/' do
  "SINATRA IS READY on port: #{settings.port}"
end
