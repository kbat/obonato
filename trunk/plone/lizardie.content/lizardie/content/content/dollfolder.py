"""Definition of the Doll Folder content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from lizardie.content.interfaces import IDollFolder
from lizardie.content.config import PROJECTNAME

DollFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

DollFolderSchema['title'].storage = atapi.AnnotationStorage()
DollFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    DollFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class DollFolder(folder.ATFolder):
    """Folder to keep and show Dolls"""
    implements(IDollFolder)

    meta_type = "DollFolder"
    schema = DollFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(DollFolder, PROJECTNAME)
