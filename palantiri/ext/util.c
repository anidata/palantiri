/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

#include <Python.h>
#include "structmember.h"

#if defined(_WIN32) || defined(_WIN64)
#include <tchar.h>
#endif
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

typedef void(*SignalHandler)(int);

sig_atomic_t s_process_isalive = 1;

static PyObject* palantiriError;

typedef struct {
    PyObject_HEAD
    sig_atomic_t* m_pisalive;
} ShutdownHandler;

// No need for a traversal function as the struct does not contain
// any PyObjects

static void ShutdownHandler_dealloc(ShutdownHandler* self) {
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* ShutdownHandler_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    ShutdownHandler* self;
    self = (ShutdownHandler*)type->tp_alloc(type, 0);
    if(self != NULL) {
        self->m_pisalive = &s_process_isalive;
    }

    return (PyObject*)self;
}

static void shutdownsignal_wrapper(int signum, SignalHandler handler) {
#if defined(_WIN32) || defined(_WIN64)
    signal(signum, handler);
#else
    // On a unix OS st SA_RESTART to ensure that all slow sys calls are
    // resumed after the signal is handled
    struct sigaction new_action;
    struct sigaction old_action;

    new_action.sa_flags = SA_RESTART;
    new_action.sa_handler = handler;
    sigemptyset(&new_action.sa_mask);
    if(sigaction(signum, &new_action, &old_action)) {
        PyErr_SetString(palantiriError, "error initializing handler!");
    }
#endif
}

static void ShutdownHandler_cleanshutdown(int signum) {
    if(!s_process_isalive)
        exit(-1);

    s_process_isalive = 0;
}

static int ShutdownHandler_init(ShutdownHandler* self, PyObject* args, PyObject* kwds) {
    int signum;
    static char* kwds_list[] = {"signum", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwds_list, &signum)) {
        PyErr_SetString(palantiriError, "error parsing arguments expected signum=<int>!");
    }
    if(!signum) {
        signum = 2;
    }
    shutdownsignal_wrapper(signum, ShutdownHandler_cleanshutdown);
    return 0;
}

static PyObject* ShutdownHandler_set(ShutdownHandler* self) {
    if(*(self->m_pisalive)) {
        *(self->m_pisalive) = 0;
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyObject* ShutdownHandler_add_signal(ShutdownHandler* self, PyObject* args) {
    int signum;
    if(!PyArg_ParseTuple(args, "i", &signum)) {
        PyErr_SetString(palantiriError, "error parsing arguments expected integer!");
    }
    shutdownsignal_wrapper(signum, ShutdownHandler_cleanshutdown);
    Py_RETURN_TRUE;
}

static PyObject* ShutdownHandler_setisalive(ShutdownHandler* self, PyObject* value, void* data) {
    if(value == NULL) {
        PyErr_SetString(palantiriError, "argument provided is NULL!");
    }
    if(!PyBool_Check(value)) {
        PyErr_SetString(palantiriError, "argument provided must be a boolean value!");
    }
    if(PyObject_IsTrue(value)) {
        *self->m_pisalive = 1;
        Py_RETURN_TRUE;
    } else {
        *self->m_pisalive = 0;
        Py_RETURN_FALSE;
    }
}

static PyObject* ShutdownHandler_getisalive(ShutdownHandler* self) {
    if(*(self->m_pisalive)) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

static PyGetSetDef ShutdownHandler_getsetters[] = {
    {"isalive", (getter)ShutdownHandler_getisalive,
     (setter)ShutdownHandler_setisalive, "signal flag", NULL},
    {NULL}
};

static PyMethodDef ShutdownHandler_methods[] = {
    {"set", (PyCFunction)ShutdownHandler_set, METH_NOARGS, "Set the shutdown flag"},
    {"add_signal", (PyCFunction)ShutdownHandler_add_signal, METH_VARARGS,
        "Add another signal to handle"},
    {NULL}
};

static PyTypeObject ShutdownHandlerType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "testutil.util.ShutdownHandler",     /* tp_name */
    sizeof(ShutdownHandler),             /* tp_basicsize */
    0,                                   /* tp_itemsize */
    (destructor)ShutdownHandler_dealloc, /* tp_dealloc */
    0,                                   /* tp_print */
    0,                                   /* tp_getattr */
    0,                                   /* tp_setattr */
    0,                                   /* tp_reserved */
    0,                                   /* tp_repr */
    0,                                   /* tp_as_number */
    0,                                   /* tp_as_sequence */
    0,                                   /* tp_as_mapping */
    0,                                   /* tp_hash  */
    0,                                   /* tp_call */
    0,                                   /* tp_str */
    0,                                   /* tp_getattro */
    0,                                   /* tp_setattro */
    0,                                   /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,             /* tp_flags */
    "Signal shutdown handler",           /* tp_doc */
    0,                                   /* tp_traverse */
    0,                                   /* tp_clear */
    0,                                   /* tp_richcompare */
    0,                                   /* tp_weaklistoffset */
    0,                                   /* tp_iter */
    0,                                   /* tp_iternext */
    ShutdownHandler_methods,             /* tp_methods */
    0,                                   /* tp_members */
    ShutdownHandler_getsetters,          /* tp_getset */
    0,                                   /* tp_base */
    0,                                   /* tp_dict */
    0,                                   /* tp_descr_get */
    0,                                   /* tp_descr_set */
    0,                                   /* tp_dictoffset */
    (initproc)ShutdownHandler_init,      /* tp_init */
    0,                                   /* tp_alloc */
    ShutdownHandler_new,                 /* tp_new */
};

static PyModuleDef shutdownmodule = {
    PyModuleDef_HEAD_INIT,
    "testutil.util",
    "Utility methods for the project",
    -1,
    NULL, NULL, NULL, NULL, NULL
};

#ifndef PyMODINIT_FUNC
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC PyInit_util(void) {
    PyObject* module;

    if(PyType_Ready(&ShutdownHandlerType) < 0) {
        PyErr_SetString(palantiriError, "ShutdownHandlerType is not ready!");
    }

    module = PyModule_Create(&shutdownmodule);

    if(module == NULL) {
        PyErr_SetString(palantiriError, "module object is NULL");
    }
    palantiriError = PyErr_NewException("palantiri.error", NULL, NULL);
    Py_INCREF(palantiriError);

    Py_INCREF(&ShutdownHandlerType);
    PyModule_AddObject(module, "ShutdownHandler", (PyObject*)&ShutdownHandlerType);
    return module;
}
