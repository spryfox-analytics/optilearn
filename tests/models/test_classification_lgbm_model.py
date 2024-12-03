import pytest
from unittest.mock import Mock
import numpy as np
from optilearn.models.classification_lgbm import ClassificationLGBM
from tests.models.model_fixtures import mock_u_func, mock_loss_func, BASE_CONFIG, BATCH_SIZE, get_mock_values


@pytest.fixture
def mock_lgbm_moo_config():
    BASE_CONFIG["model_config"] = {
        "model_type": "lgbm",
        "torch_interface": False,
        "params": {
            "n_jobs": -1,
            "verbose": -1,
            # "early_stopping_round": 5,
            "max_depth": 5
        }
    }
    return BASE_CONFIG


@pytest.fixture
def mock_lgbm_config():
    BASE_CONFIG["p_dim"] = 1
    BASE_CONFIG["model_config"] = {
        "model_type": "lgbm",
        "torch_interface": False,
        "params": {
            "n_jobs": -1,
            "verbose": -1,
            # "early_stopping_round": 5,
            "max_depth": 5
        }
    }
    return BASE_CONFIG


def test_classification_lgbm_forward(mock_lgbm_config, mock_u_func, mock_loss_func):
    model = ClassificationLGBM(config=mock_lgbm_config, u_func=mock_u_func, loss_criterion=mock_loss_func)
    states, preds, labels, prefs = get_mock_values(mock_lgbm_config)
    model.make_step(states=states, labels=labels, preds=preds, prefs=prefs)
    probs = model.forward(state=states, pref=prefs)
    assert probs.shape == (BATCH_SIZE, mock_lgbm_config["a_dim"])
    assert ((probs >= 0) & (probs <= 1)).all()
    assert (probs.sum(axis=1) == 1).all()


def test_classification_lgbm_choose_action(mock_lgbm_config, mock_u_func, mock_loss_func):
    model = ClassificationLGBM(config=mock_lgbm_config, u_func=mock_u_func, loss_criterion=mock_loss_func)
    states, preds, labels, prefs = get_mock_values(mock_lgbm_config)
    model.make_step(states=states, labels=labels, preds=preds, prefs=prefs)
    actions, probs = model.choose_action(state=states, pref=prefs)
    assert actions.shape == (BATCH_SIZE,)
    assert actions.dtype == np.int64
    assert ((actions >= 0) & (actions <= mock_lgbm_config["a_dim"])).all()
    assert probs.shape == (BATCH_SIZE, mock_lgbm_config["a_dim"])
    assert ((probs >= 0) & (probs <= 1)).all()
    assert (probs.sum(axis=1) > 0.9999).all()



def test_classification_lgbm_make_step(mock_lgbm_config, mock_u_func, mock_loss_func):
    model = ClassificationLGBM(config=mock_lgbm_config, u_func=mock_u_func, loss_criterion=mock_loss_func)
    states, preds, labels, prefs = get_mock_values(mock_lgbm_config)
    loss = model.make_step(states=states, labels=labels, preds=preds, prefs=prefs)
    assert isinstance(loss, float)
