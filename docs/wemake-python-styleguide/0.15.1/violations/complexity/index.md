
These checks find flaws in your application design.

We try to stick to "the magical 7 ± 2 number" when counting things.
https://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two

That's how many objects we can keep in our memory at a time.
We try hard not to exceed the memory capacity limit.

You can also find interesting reading about "Cognitive complexity":
https://www.sonarsource.com/docs/CognitiveComplexity.pdf

Note:
    Simple is better than complex.
    Complex is better than complicated.

See also:
    https://sobolevn.me/2019/10/complexity-waterfall

.. currentmodule:: wemake_python_styleguide.violations.complexity

Summary
-------

.. autosummary::
   :nosignatures:

   JonesScoreViolation
   TooManyImportsViolation
   TooManyModuleMembersViolation
   TooManyImportedNamesViolation
   OverusedExpressionViolation
   TooManyLocalsViolation
   TooManyArgumentsViolation
   TooManyReturnsViolation
   TooManyExpressionsViolation
   TooManyMethodsViolation
   TooManyBaseClassesViolation
   TooManyDecoratorsViolation
   TooManyAwaitsViolation
   TooManyAssertsViolation
   TooDeepAccessViolation
   TooDeepNestingViolation
   LineComplexityViolation
   TooManyConditionsViolation
   TooManyElifsViolation
   TooManyForsInComprehensionViolation
   TooManyExceptCasesViolation
   OverusedStringViolation
   TooLongYieldTupleViolation
   TooLongCompareViolation
   TooLongTryBodyViolation
   TooManyPublicAttributesViolation
   CognitiveComplexityViolation
   CognitiveModuleComplexityViolation
   TooLongCallChainViolation
   TooComplexAnnotationViolation
   TooManyImportedModuleMembersViolation
   TooLongTupleUnpackViolation
   TooComplexFormattedStringViolation
   TooManyRaisesViolation

Module complexity
-----------------

.. autoclass:: JonesScoreViolation
.. autoclass:: TooManyImportsViolation
.. autoclass:: TooManyModuleMembersViolation
.. autoclass:: TooManyImportedNamesViolation
.. autoclass:: OverusedExpressionViolation

Structure complexity
--------------------

.. autoclass:: TooManyLocalsViolation
.. autoclass:: TooManyArgumentsViolation
.. autoclass:: TooManyReturnsViolation
.. autoclass:: TooManyExpressionsViolation
.. autoclass:: TooManyMethodsViolation
.. autoclass:: TooManyBaseClassesViolation
.. autoclass:: TooManyDecoratorsViolation
.. autoclass:: TooManyAwaitsViolation
.. autoclass:: TooManyAssertsViolation
.. autoclass:: TooDeepAccessViolation
.. autoclass:: TooDeepNestingViolation
.. autoclass:: LineComplexityViolation
.. autoclass:: TooManyConditionsViolation
.. autoclass:: TooManyElifsViolation
.. autoclass:: TooManyForsInComprehensionViolation
.. autoclass:: TooManyExceptCasesViolation
.. autoclass:: OverusedStringViolation
.. autoclass:: TooLongYieldTupleViolation
.. autoclass:: TooLongCompareViolation
.. autoclass:: TooLongTryBodyViolation
.. autoclass:: TooManyPublicAttributesViolation
.. autoclass:: CognitiveComplexityViolation
.. autoclass:: CognitiveModuleComplexityViolation
.. autoclass:: TooLongCallChainViolation
.. autoclass:: TooComplexAnnotationViolation
.. autoclass:: TooManyImportedModuleMembersViolation
.. autoclass:: TooLongTupleUnpackViolation
.. autoclass:: TooComplexFormattedStringViolation
.. autoclass:: TooManyRaisesViolation

