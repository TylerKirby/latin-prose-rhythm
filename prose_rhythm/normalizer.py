# -*- coding: utf-8 -*-
"""
Normalize Latin text for preprocessing.

The module assume that the text is already macronized and is utf 8 encoded.
"""
import regex as re

DEFAULT_PUNC = ['.', '?', '!', ';', ':']
DEFAULT_ABBREVIATIONS = ['Agr.', 'Ap.', 'A.', 'K.', 'D.', 'F.', 'C.',
                       'Cn.', 'L.', 'Mam.', 'M\'', 'M.', 'N.', 'Oct.',
                       'Opet.', 'Post.', 'Pro.', 'P.', 'Q.', 'Sert.',
                       'Ser.', 'Sex.', 'S.', 'St.', 'Ti.', 'T.', 'V.',
                       'Vol.', 'Vop.', 'Pl.']

class Normalizer(object):

    def __init__(self, text, punctuation=DEFAULT_PUNC, replace_abbrev=True, abbrev=DEFAULT_ABBREVIATIONS):
        self.text = text
        self.punctuation = punctuation
        self.replace_abbrev = replace_abbrev
        self.abbrev = abbrev

    def _replace_abbreviations(self):
        """
        Replace abbreviations
        :return:
        """
        for abbrev in self.abbrev:
            self.text = self.text.replace(abbrev, 'abbrev')
        return self.text

    def normalize(self):
        """
        Normalize text.
        Punctuation is standardized with the supplied punctuation list.
        :return: normalized text
        """
        default_seperator = '.'

        for punc in self.punctuation:
            self.text = self.text.replace(punc, default_seperator)

        if (self.replace_abbrev):
            self.text = self._replace_abbreviations()

        self.text = re.sub(r'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})', '', self.text)
        self.text = self.text.lower()
        self.text = re.sub(r'[^a-z.\sāēīōū]', '', self.text)
        self.text = re.sub(r'\s{2}', ' ', self.text)
        return self.text

if __name__ == '__main__':
    test_text = 'Galliā est omnīs dīvīsa in partēs trēs quārum ūnam incolunt Belgae aliam Aquītānī tertiam quī ipsōrum lingua Celtae nostra Gallī appellantur. hī omnēs linguā īnstitūtīs lēgibus inter sē differunt. Gallōs ab Aquītānīs Garunna flūmen ā Belgīs Matrona et Sēquana dīvidit. hōrum omnium fortissimī sunt Belgae proptereā quod ā cultū atque hūmānitāte prōvinciae longissimē absunt minimēque ad eōs mercātōrēs saepe commeant atque ea quae ad effēminandōs animōs pertinent important proximīque sunt Germānīs quī trāns Rhēnum incolunt quibuscum continenter bellum gerunt. quā dē causā Helvētiī quoque reliquōs Gallōs virtūte praecēdunt quod ferē cotīdiānīs proeliīs cum Germānīs contendunt cum aut suīs fīnibus eōs prohibent aut ipsī in eōrum fīnibus bellum gerunt. eōrum ūna pars quam Gallōs obtinēre dictum est initium capit ā flūmine Rhodanō continētur Garunna flūmine Ōceanō fīnibus Belgārum attingit etiam ab Sēquanīs et Helvētiīs flūmen Rhēnum vergit ad  septentriōnēs. Belgae ab extrēmīs Galliae fīnibus oriuntur pertinent ad īnferiōrem partem flūminis Rhēnī spectant in septentriōnem et orientem sōlem. Aquītānia ā Garunnā flūmine ad Pȳrēnaeōs montēs et eam partem Ōceanī quae est ad Hispāniam pertinet spectat inter occāsum sōlis et septentriōnēs. Apud Helvētiōs longē nōbilissimus fuit et dītissimus Orgetorix. is M. Messāla et P. M. Pīsōne cōnsulibus rēgnī cupiditāte inductus conjūrātiōnem nōbilitātis fēcit et cīvitātī persuāsit ut dē fīnibus suīs cum omnibus cōpiīs exīrent perfacile esse cum virtūte omnibus praestārent tōtīus Galliae imperiō potīrī. id hoc facilius iīs persuāsit quod undique locī nātūra Helvētiī continentur ūna ex parte flūmine Rhēnō lātissimō atque altissimō quī agrum Helvētium ā Germānīs dīvidit altera ex parte monte Jūrā altissimō quī est inter Sēquanōs et Helvētiōs tertia lacū Lemannō et flūmine Rhodanō quī prōvinciam nostram ab Helvētiīs dīvidit. hīs rēbus fīēbat ut et minus lātē vagārentur et minus facile fīnitimīs bellum īnferre possent quā ex parte hominēs bellandī cupidī magnō dolōre adficiēbantur. prō multitūdine autem hominum et prō glōriā bellī atque fortitūdinis angustōs sē fīnēs habēre arbitrābantur quī in longitūdinem mīlia passuum ccxl in lātitūdinem clxxx patēbant. Hīs rēbus adductī et auctōritāte Orgetorigis permōtī cōnstituērunt ea quae ad proficīscendum pertinērent comparāre jūmentōrum et carrōrum quam maximum numerum coemere sēmentēs quam maximās facere ut in itinere cōpia frūmentī suppeteret cum proximīs cīvitātibus pācem et amīcitiam cōnfirmāre. ad eās rēs cōnficiendās biennium sibi satis esse dūxērunt in  tertium annum profectiōnem lēge cōnfirmant. ad eās rēs cōnficiendās Orgetorix dēligitur. is sibi lēgātiōnem ad cīvitātēs suscēpit. in eō itinere persuādet Castīcō Catamantaloedis fīliō Sēquanō cūjus pater rēgnum in Sēquanīs multōs annōs obtinuerat et ab senātū populī Rōmānī amīcus appellātus erat ut rēgnum in cīvitāte suā occupāret quod pater ante habuerat itemque Dumnorigī Haeduō frātrī Dīviciācī quī eō tempore prīncipātum in cīvitāte obtinēbat ac maximē plēbī acceptus erat ut īdem cōnārētur persuādet eīque fīliam suam in mātrimōnium dat. perfacile factū esse illīs probat cōnāta perficere proptereā quod ipse suae cīvitātis imperium obtentūrus esset nōn esse dubium quīn tōtīus Galliae plūrimum Helvētiī possent sē suīs cōpiīs suōque exercitū illīs rēgna conciliātūrum cōnfirmat. hāc ōrātiōne adductī inter sē fidem et jūs jūrandum dant et rēgnō occupātō per trēs potentissimōs ac firmissimōs populōs tōtīus Galliae sēsē potīrī posse spērant. Ea rēs est Helvētiīs per indicium ēnūntiāta. mōribus suīs Orgetorigem ex vinculīs causam dīcere coēgērunt damnātum poenam sequī oportēbat ut ignī cremārētur. diē cōnstitūtā causae dictiōnis Orgetorix ad jūdicium omnem suam familiam ad hominum mīlia decem undique coēgit et omnēs clientēs obaerātōsque suōs quōrum magnum numerum habēbat eōdem condūxit per eōs nē causam dīceret sē ēripuit. cum cīvitās ob eam rem incitātā armīs jūs suum exsequī cōnārētur multitūdinemque hominum ex agrīs magistrātūs cōgerent Orgetorix mortuus est neque abest suspīciō ut Helvētiī arbitrantur quīn ipse sibi mortem cōnscīverit. Post ējus mortem nihilōminus Helvētiī id quod cōnstituerant facere cōnantur ut ē fīnibus suīs exeant. ubi  jam sē ad eam rem parātōs esse arbitrātī sunt oppida sua omnia numerō ad duodecim vīcōs ad quadringentōs reliqua prīvāta aedificia incendunt frūmentum omne praeter quod sēcum portātūrī erant combūrunt ut domum reditiōnis spē sublāta parātiōrēs ad omnia perīcula subeunda essent trium mēnsum molita cibāria sibi quemque domō efferre jubent. persuādent Rauracīs et Tulingīs et Latobrigīs fīnitimīs utī eōdem ūsī cōnsiliō oppidīs suīs vīcīsque exustīs ūna cum iīs proficīscantur Boiōsque quī trāns Rhēnum incoluerant et in agrum Nōricum trānsierant Norēiamque oppugnābant receptōs ad sē sociōs sibi adscīscunt.'
    test_class = Normalizer(test_text, ['.', ';'])
    print(test_class.normalize())
