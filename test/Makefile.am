check_SCRIPTS=run-test.sh
TEST_EXTENSIONS = \
	.sh \
	$(NULL)

AM_TESTS_ENVIRONMENT= \
	src=${srcdir}; export src; \
	EXEEXT=${EXEEXT}; export EXEEXT; \
	$(NULL)

SH_LOG_COMPILER = sh

TESTS=run-test.sh

TESTDATA=4x6.pcf 8x16.pcf out.expected fonts.conf.in

EXTRA_DIST=$(check_SCRIPTS) $(TESTDATA)

CLEANFILES=
