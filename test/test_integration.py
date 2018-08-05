"""
Tests spanning multiple modules.
"""
import codecs


from prose_rhythm.preprocessor import Preprocessor
from prose_rhythm.analyze import Analyze

analyze = Analyze()


def test_pro_milone_1_6():
    with codecs.open('test/pro_milone_1-6.txt', 'r', encoding='utf8') as f:
        text = f.read()
    target = [
    ('etsī vereor, jūdicēs, nē turpe sit prō fortissimō virō dīcere incipientem timēre minimēque deceat, cum 00000 annius ipse magis dē reī pūblicae salūte quam dē suā perturbētur, mē ad ējus causam parem animī magnitūdinem adferre nōn posse, tamen haec novī jūdicī nova fōrma terret oculōs quī, quōcumque incīdērunt, veterem cōnsuētūdinem forī et pristīnum mōrem jūdiciōrum requīrunt',

      '-uu--u-x'),

     (' nōn enim corōna cōnsessus vester cīnctus est, ut solēbat', '--u--u-x'),

     (' nōn ūsitātā frequentiā stīpātī sumus', '-u----ux'),

     (' nōn illa praesidia quae prō templīs omnibus cernitis, etsī contrā vim conlocāta sunt, nōn adferunt tamen ōrātōrī terrōris aliquid, ut in forō et in jūdiciō, quamquam praesidiīs salūtāribus et necessāriīs saeptī sumus, tamen nē nōn timēre quidem sine aliquō timōre possīmus',

      'u-u-u--x'),

     (' quae sī opposita mīlōnī putārem, cēderem temporī, jūdicēs, nec enim inter tantam vim armōrum exīstimārem esse ōrātiōnī locum',

      '---u--ux'),

     (' sed mē recreat et reficit 00000 pompēī, sapientissimī et jūstissimī virī, cōnsilium, quī profectō nec jūstitiae suae putāret esse, quem reum sententiīs jūdicum trādidisset, eundem tēlīs mīlitum dēdere, nec sapientiae temeritātem concītatae multitūdinis auctōritāte pūblicā armāre',

      'u-u-u--x'),

     (' quam ob rem illa arma, centuriōnēs, cohortēs nōn perīculum nōbīs, sed praesidium dēnūntiant, neque sōlum ut quiētō, sed etiam ut magnō animō sīmus hortantur, nec auxilium modo dēfēnsiōnī meae vērum etiam silentium pollicentur',

      'u-u--u-x'),

     (' relīquā vērō multitūdō, quae quidem est cīvium, tōta nostra est, nec eōrum quisquam quōs undique intuentīs, unde aliquā forī pars aspicī potest, et hūjus exitum jūdicī exspectantīs vidētis, nōn cum virtūtī milōnis favet, tum dē sē, dē līberīs suīs, dē patriā, dē fortūnīs hodiernō diē dēcertārī putat',

      'u-----ux'),

     (' vnum genus est adversum īnfēstumque nōbīs eōrum quōs 00000 clōdī furor rapīnīs et incendiīs et omnibus exitiīs pūblicīs pāvit',

      'uu--u--x'),

     (' quī hesternā etiam contiōne incitātī sunt ut vōbīs vōce praeīrent quid jūdicārētis',

      '----u--x'),

     (' quōrum clāmor sī quī forte fuerit, admonēre vōs dēbēbit ut eum cīvem retineātis quī semper genus illud hominum clāmōrēsque maximōs prae vestrā salūte neglēxit',

      '--u-u--x'),

     (' quam ob rem adeste animīs, jūdicēs, et timōrem, sī quem habētis, dēpōnite',

      '-u----ux'),

     (' nam sī umquam dē bonīs et fortibus virīs, sī umquam dē bene meritīs cīvibus potestās vōbīs jūdicandī fuit, sī dēnique umquam locus amplissimōrum ōrdinum dēlēctīs virīs datus est ut sua studia ergā fortīs et bonōs cīvīs, quae voltū et verbīs saepe significāssent, rē et sententiīs dēclārārent, hocc profectō tempore eam potestātem omnem vōs habētis ut statuātis utrum nōs quī semper vestrae auctōritātī dēditī fuimus semper miserī lūgeāmus an diū vexātī ā perditissimīs cīvibus alīquandō per vōs ac per vestram fidem, virtūtem sapientiamque recreēmur',

      '-u-uuu-x'),

     (' quid enim nōbīs duōbus, jūdicēs, labōriōsius, quid magis sollicitum, magis exercitum dīcī aut fingī potest, quī spē amplissimōrum praemiōrum ad rem pūblicam adductī metū crūdēlissimōrum suppliciōrum carēre nōn possumus',

      '-u-u--ux'),

     (' equidem cēterās tempestātēs et procellās in illīs dumtaxat flūctibus contiōnum semper putāvī milōnī esse subeundās, quia semper prō bonīs contrā improbōs sēnserat, in jūdiciō vērō et in eō cōnsiliō in quō ex conjūnctīs ōrdinibus amplissimī virī jūdicārent numquam exīstimāvī spem ūllam esse habitūrōs milōnis inimīcōs ad ējus nōn modo salūtem exstinguendam sed etiam glōriam per tālīs virōs īnfringendam',

      '--u----x'),

     (' quamquam in hāc causā jūdicēs, 00000 annī tribūnātū rēbusque omnibus prō salūte reī pūblicae gestīs ad hūjus crīminis dēfēnsiōnem nōn abūtēmur',

      'u---u--x'),

     (' nisi oculīs vīderītis īnsidiās mīlōnī ā clōdiō esse factās, nec dēprecātūrī sumus ut crīmen hocc nōbīs propter multa praeclārā in rem pūblicam merita condōnētis, nec postulātūrī ut, quia mors 00000 clōdī salūs vestra fuerit, idcircō eam virtūtī milōnis potius quam populī rōmānī fēlīcitātī adsignētis',

      '--u----x'),

     (' sīn illīus īnsidiae clāriōrēs hāc lūce fuerint, tum dēnique obsecrābō obtestāborque vōs, jūdicēs, sī cētera āmīsimus, hocc nōbīs saltem ut relinquātur, vītam ab inimīcōrum audācia tēlīsque ut impūne liceat dēfendere',

      'uuu---ux')
    ]
    preprocess = Preprocessor(text=text)
    tokens = preprocess.tokenize()
    analysis = analyze.get_rhythms(tokens)
    assert analysis == target