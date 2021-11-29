from modeltranslation.translator import translator, TranslationOptions

from .models import HealthProblem

class HealthTranslationOption(TranslationOptions):
    fields = ('title', 'description')

translator.register(HealthProblem, HealthTranslationOption)