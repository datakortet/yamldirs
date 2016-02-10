import invoke
from dktasklib import version
from dktasklib import docs
from dktasklib import publish


ns = invoke.Collection(version, docs, publish)
