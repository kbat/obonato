# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s cl.content -t test_component.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src cl.content.testing.CL_CONTENT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/cl/content/tests/robot/test_component.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Component
  Given a logged-in site administrator
    and an add Component form
   When I type 'My Component' into the title field
    and I submit the form
   Then a Component with the title 'My Component' has been created

Scenario: As a site administrator I can view a Component
  Given a logged-in site administrator
    and a Component 'My Component'
   When I go to the Component view
   Then I can see the Component title 'My Component'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Component form
  Go To  ${PLONE_URL}/++add++Component

a Component 'My Component'
  Create content  type=Component  id=my-component  title=My Component

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Component view
  Go To  ${PLONE_URL}/my-component
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Component with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Component title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
