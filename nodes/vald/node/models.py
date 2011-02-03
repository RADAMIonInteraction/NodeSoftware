from django.db.models import *
from vamdctap.bibtextools import *

class Species(Model):
    id = IntegerField(primary_key=True, db_index=True)
    name = CharField(max_length=10, db_index=True)
    ion = PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    mass = DecimalField(max_digits=8, decimal_places=5) 
    massno = PositiveSmallIntegerField(null=True, blank=True)
    ionen = DecimalField(max_digits=7, decimal_places=3) 
    solariso = DecimalField(max_digits=5, decimal_places=4) 
    ncomp = PositiveSmallIntegerField(null=True, blank=True)
    atomic = PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    isotope = PositiveSmallIntegerField(null=True, blank=True)
    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.name)
    class Meta:
        db_table = u'species'

class Reference(Model):
    dbref = CharField(max_length=64, primary_key=True, db_index=True)
    #bibref = CharField(max_length=25)
    #title = CharField(max_length=256, null=True)
    #author = CharField(max_length = 256, null=True)
    #category = CharField(max_length=128, null=True)
    #year = PositiveSmallIntegerField(null=True)
    #journal = CharField(max_length=256, null=True)
    #volume = CharField(max_length=64, null=True)
    #pages = CharField(max_length=64, null=True)
    #pagebegin = PositiveSmallIntegerField(null=True)
    #pageend = PositiveSmallIntegerField(null=True)
    #url = CharField(max_length=512, null=True)  
    bibtex = CharField(max_length=1024, null=True)

    def XML(self):
        return Entry2XML( getEntryFromString(self.bibtex) )

    class Meta:
        db_table = u'references'
    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.dbref)

class LineList(Model):
    id = IntegerField(primary_key=True, db_index=True)
    references = ManyToManyField(Reference)
    srcfile = CharField(max_length=128)
    srcfile_ref = CharField(max_length=128, null=True)
    speclo = ForeignKey(Species,related_name='islowerboundspecies_source',db_column='speclo',null=True)
    spechi = ForeignKey(Species,related_name='isupperboundspecies_source',db_column='spechi',null=True)
    listtype = PositiveSmallIntegerField(null=True,blank=True)
    r1 = PositiveSmallIntegerField(null=True, blank=True)
    r2 = PositiveSmallIntegerField(null=True, blank=True)
    r3 = PositiveSmallIntegerField(null=True, blank=True)
    r4 = PositiveSmallIntegerField(null=True, blank=True)
    r5 = PositiveSmallIntegerField(null=True, blank=True)
    r6 = PositiveSmallIntegerField(null=True, blank=True)
    r7 = PositiveSmallIntegerField(null=True, blank=True)
    r8 = PositiveSmallIntegerField(null=True, blank=True)
    r9 = PositiveSmallIntegerField(null=True, blank=True)
    srcdescr = CharField(max_length=128, blank=True, null=True)
    def __unicode__(self):
        return u'ID%s: %s'%(self.id,self.srcdescr)        
    class Meta:
        db_table = u'linelists'


class State(Model):
    id = CharField(max_length=255, primary_key=True, db_index=True)
    species = ForeignKey(Species)  

    energy = DecimalField(max_digits=15, decimal_places=4,null=True,blank=True, db_index=True) 
    lande = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    coupling = CharField(max_length=2, null=True,blank=True)
    term = CharField(max_length=56, null=True,blank=True)
    j = DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True,blank=True)
    l = DecimalField(max_digits=3, decimal_places=1,db_column=u'L', null=True,blank=True)
    s = DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True,blank=True)
    p = DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True,blank=True)
    j1 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True,blank=True)
    j2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True,blank=True)
    k = DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True,blank=True)
    s2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True,blank=True)
    jc = DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True,blank=True)

    energy_ref = ForeignKey(LineList, related_name='isenergyref_state')
    lande_ref = ForeignKey(LineList, related_name='islanderef_state')
    level_ref = ForeignKey(LineList, related_name='islevelref_state')
    def __unicode__(self):
        return u'ID:%s Eng:%s'%(self.id,self.energy)
    class Meta:
        db_table = u'states'

class Transition(Model):
    id = IntegerField(primary_key=True)
    upstate = ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True)
    lostate = ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True)
    
    vacwave = DecimalField(max_digits=20, decimal_places=8, db_index=True) 
    airwave = DecimalField(max_digits=20, decimal_places=8, db_index=True) 
    species = ForeignKey(Species,db_column='species')
    loggf = DecimalField(max_digits=8, decimal_places=3,null=True,blank=True)
    landeff = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammarad = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammastark = DecimalField(max_digits=7, decimal_places=3,null=True,blank=True)     
    gammawaals = DecimalField(max_digits=6, decimal_places=3,null=True,blank=True)
    sigmawaals = IntegerField(null=True,blank=True)                               
    alphawaals = DecimalField(max_digits=6, decimal_places=3,null=True,blank=True) 
    accur = CharField(max_length=11, blank=True,null=True)
    comment = CharField(max_length=128, null=True,blank=True)

    srctag = ForeignKey(Reference)
    wave_ref = ForeignKey(LineList, related_name='iswaveref_trans')
    loggf_ref = ForeignKey(LineList, related_name='isloggfref_trans')
    lande_ref = ForeignKey(LineList, related_name='islanderef_trans')
    gammarad_ref = ForeignKey(LineList, related_name='isgammaradref_trans')
    gammastark_ref = ForeignKey(LineList, related_name='isgammastarkref_trans')
    waals_ref = ForeignKey(LineList, related_name='iswaalsref_trans')

    def __unicode__(self):
        return u'ID:%s Wavel: %s'%(self.id,self.vacwave)
    class Meta:
        db_table = u'transitions'



###############################
## Logging Queries
###############################
class Query(Model):
    qid=CharField(max_length=6,primary_key=True,db_index=True)
    datetime=DateTimeField(auto_now_add=True)
    query=CharField(max_length=512)

import string, random
class LogManager(Manager):
    """
    Handles log object searches
    """    
    def makeQID(self, length=6, chars=string.letters + string.digits):
        return ''.join([random.choice(chars) for i in xrange(length)])
    def create(self, request):
        """
        Create a query log based on a request
        """
        log = self.model(qid=self.makeQID(),
                         query=None, #TODO!
                         request=request)
        pass

    
class Log(Model):
    """
    Stores data of a query
    """
    qid = CharField(max_length=128)
    datetime = datetime=DateTimeField(auto_now_add=True)
    query = ForeignKey(Query, related_name='dbquery', db_column='query')
    request = CharField(max_length=1014)

    objects = LogManager()
