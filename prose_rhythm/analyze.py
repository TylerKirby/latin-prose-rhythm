# -*- coding: utf-8 -*-
"""
Analyze Latin prose rhythms.

Module assumes that texts are preprocessed before analyzing.
"""

from prose_rhythm.preprocessor import Preprocessor
import pprint

class Analyze(object):
    """
    Analyze Latin prose rhythms.
    """

    def __init__(self, clausula_length=8, include_short_clausula=False):
        self.clausula_length = clausula_length
        self.include_short_clausula = include_short_clausula

    def get_rhythms(self, tokens):
        """
        Return a flat list of rhythms.
        Desired clausula length is passed as a parameter. Clausula shorter than the specified
        length can be exluded.
        :return:
        """
        clausulae = []
        for sentence in tokens['text']:
            sentence_clausula = ''
            if not sentence['contains_numeral'] and not sentence['contains_abbrev']:
                for word in reversed(sentence['structured_sentence']):
                    for syllable in reversed(word['syllables']):
                        if len(sentence_clausula) < self.clausula_length:
                            if syllable['long_by_nature'] or syllable['long_by_position'][0]:
                                sentence_clausula = '-' + sentence_clausula
                            else:
                                sentence_clausula = 'u' + sentence_clausula
                sentence_clausula = sentence_clausula[:-1] + 'x'
                clausulae.append((sentence['plain_text_sentence'], sentence_clausula))

        if not self.include_short_clausula:
            return [clausula for clausula in clausulae if len(clausula) == self.clausula_length]

        return clausulae


if __name__ == "__main__":
    text = """Etsī vereor, jūdicēs, nē turpe sit prō fortissimō virō 
dīcere incipientem timēre minimēque deceat, cum T. Annius 
ipse magis dē reī pūblicae salūte quam dē suā perturbētur, 
mē ad ējus causam parem animī magnitūdinem adferre nōn 
posse, tamen haec novī jūdicī nova fōrma terret oculōs quī, 
quōcumque incīdērunt, veterem cōnsuētūdinem forī et pristī-
num mōrem jūdiciōrum requīrunt. Nōn enim corōna cōn-
sessus vester cīnctus est, ut solēbat; nōn ūsitātā frequentiā 
stīpātī sumus; nōn illa praesidia quae prō templīs omnibus 
cernitis, etsī contrā vim conlocāta sunt, nōn adferunt tamen 
ōrātōrī terrōris aliquid, ut in forō et in jūdiciō, quamquam 
praesidiīs salūtāribus et necessāriīs saeptī sumus, tamen nē 
nōn timēre quidem sine aliquō timōre possīmus. Quae sī 
opposita Mīlōnī putārem, cēderem temporī, jūdicēs, nec 
enim inter tantam vim armōrum exīstimārem esse ōrātiōnī 
locum. Sed mē recreat et reficit Cn. Pompēī, sapientissimī 
et jūstissimī virī, cōnsilium, quī profectō nec jūstitiae suae 
putāret esse, quem reum sententiīs jūdicum trādidisset, eun-  
dem tēlīs mīlitum dēdere, nec sapientiae temeritātem concī-
tatae multitūdinis auctōritāte pūblicā armāre. Quam ob 
rem illa arma, centuriōnēs, cohortēs nōn perīculum nōbīs, 
sed praesidium dēnūntiant, neque sōlum ut quiētō, sed 
etiam ut magnō animō sīmus hortantur, nec auxilium modo 
dēfēnsiōnī meae vērum etiam silentium pollicentur. Relī-
quā vērō multitūdō, quae quidem est cīvium, tōta nostra est, 
nec eōrum quisquam quōs undique intuentīs, unde aliquā 
forī pars aspicī potest, et hūjus exitum jūdicī exspectantīs 
vidētis, nōn cum virtūtī Milōnis favet, tum dē sē, dē līberīs 
suīs, dē patriā, dē fortūnīs hodiernō diē dēcertārī putat. 
Vnum genus est adversum īnfēstumque nōbīs eōrum quōs 
P. Clōdī furor rapīnīs et incendiīs et omnibus exitiīs pūblicīs 
pāvit; quī hesternā etiam contiōne incitātī sunt ut vōbīs 
vōce praeīrent quid jūdicārētis. Quōrum clāmor sī quī 
forte fuerit, admonēre vōs dēbēbit ut eum cīvem retineātis 
quī semper genus illud hominum clāmōrēsque maximōs prae 
vestrā salūte neglēxit. Quam ob rem adeste animīs, jūdicēs, 
et timōrem, sī quem habētis, dēpōnite. Nam sī umquam dē 
bonīs et fortibus virīs, sī umquam dē bene meritīs cīvibus 
potestās vōbīs jūdicandī fuit, sī dēnique umquam locus 
amplissimōrum ōrdinum dēlēctīs virīs datus est ut sua 
studia ergā fortīs et bonōs cīvīs, quae voltū et verbīs saepe 
significāssent, rē et sententiīs dēclārārent, hoc profectō tem-
pore eam potestātem omnem vōs habētis ut statuātis utrum 
nōs quī semper vestrae auctōritātī dēditī fuimus semper 
miserī lūgeāmus an diū vexātī ā perditissimīs cīvibus alī-
quandō per vōs ac per vestram fidem, virtūtem sapientiamque 
recreēmur. Quid enim nōbīs duōbus, jūdicēs, labōriōsius, 
quid magis sollicitum, magis exercitum dīcī aut fingī potest, 
quī spē amplissimōrum praemiōrum ad rem pūblicam  
adductī metū crūdēlissimōrum suppliciōrum carēre nōn 
possumus? Equidem cēterās tempestātēs et procellās in 
illīs dumtaxat flūctibus contiōnum semper putāvī Milōnī 
esse subeundās, quia semper prō bonīs contrā improbōs 
sēnserat, in jūdiciō vērō et in eō cōnsiliō in quō ex conjūnctīs 
ōrdinibus amplissimī virī jūdicārent numquam exīstimāvī 
spem ūllam esse habitūrōs Milōnis inimīcōs ad ējus nōn 
modo salūtem exstinguendam sed etiam glōriam per tālīs 
virōs īnfringendam. Quamquam in hāc causā jūdicēs, 
T. Annī tribūnātū rēbusque omnibus prō salūte reī pūblicae 
gestīs ad hūjus crīminis dēfēnsiōnem nōn abūtēmur. Nisi 
oculīs vīderītis īnsidiās Mīlōnī ā Clōdiō esse factās, nec 
dēprecātūrī sumus ut crīmen hoc nōbīs propter multa prae-
clārā in rem pūblicam merita condōnētis, nec postulātūrī 
ut, quia mors P. Clōdī salūs vestra fuerit, idcircō eam virtūtī 
Milōnis potius quam populī Rōmānī fēlīcitātī adsignētis. 
Sīn illīus īnsidiae clāriōrēs hāc lūce fuerint, tum dēnique 
obsecrābō obtestāborque vōs, jūdicēs, sī cētera āmīsimus, 
hoc nōbīs saltem ut relinquātur, vītam ab inimīcōrum au-
dācia tēlīsque ut impūne liceat dēfendere. """
    preprocessor = Preprocessor(text=text)
    tokens = preprocessor.tokenize()
    rhythms = Analyze(include_short_clausula=False).get_rhythms(tokens)
    print(rhythms)
