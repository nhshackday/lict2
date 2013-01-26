page = require('webpage').create()

page.onLoadFinished = (status) ->
  console.log ("loaded: " + status)
  console.log page.evaluate( () ->
    return window.document.title
  )
  page.switchToChildFrame("frame1")
  console.log page.evaluate( () ->
    return window.document.title
  )
  phantom.exit()
  return null

showStatusOfAllFrames = () ->
  showStatusOfFrames()
  console.log "\n"
  return null

showStatusOfFrames = () ->
  frame_status = page.evaluate(onPage_showStatusOfFramesFunction)
  console.log frame_status.msg
  if frame_status.frame_names.length > 0
    #see if frames contain frames
    for frame_name in frame_status.frame_names
      page.switchToChildFrame(frame_name)
      showStatusOfFrames()
      page.switchToParentFrame()
  return null




onPage_showStatusOfFramesFunction = () ->
  getFramesForCurrentPage = () ->
    frames = window.document.getElementsByTagName('frame')
    frames = Array.prototype.slice.call(frames) #nodeLists are not arrays
    iframes = window.document.getElementsByTagName('iframe')
    iframes = Array.prototype.slice.call(iframes) #nodeLists are not arrays
    frames = frames.concat(iframes)
    return frames

  getFrameStatus = (frames) ->
    frame_names = []
    if frames.length > 0
      msg = "Status of all #{frames.length} frames in #{window.location.href}:"
      for frame in frames
        state = frame.contentWindow.document.readyState
        msg += "\n  frame.state=#{state}, name=#{frame.name}, src=#{frame.src}"
        frame_names.push frame.name
    else
      msg = "There are #{frames.length} frames"
      if window.name
        msg += " in the page named=#{window.name}, src=#{window.src}"
      else
        msg += " in the root page"
    return {msg, frame_names}

  frames = getFramesForCurrentPage()
  frame_status = getFrameStatus(frames)
  return frame_status


showStatusOfAllFrames()
window.setInterval(showStatusOfAllFrames,1000)

page.open("http://localhost:4000/index.html")