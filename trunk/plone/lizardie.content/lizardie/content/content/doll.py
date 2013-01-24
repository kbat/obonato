"""Definition of the Doll content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from lizardie.content.interfaces import IDoll
from lizardie.content.config import PROJECTNAME

DollSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
        

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

DollSchema['title'].storage = atapi.AnnotationStorage()
DollSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    DollSchema,
    folderish=True,
    moveDiscussion=False
)


class Doll(folder.ATFolder):
    """Doll"""
    implements(IDoll)

    meta_type = "Doll"
    schema = DollSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Doll, PROJECTNAME)
