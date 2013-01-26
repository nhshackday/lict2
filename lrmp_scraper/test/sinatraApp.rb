require 'sinatra'
require 'json'

require 'pry'

get '/test/webpage-spec-frames/index.html' do
  send_file File.join(File.dirname(__FILE__), '/test/webpage-spec-frames/index.html', params[:any])
end
