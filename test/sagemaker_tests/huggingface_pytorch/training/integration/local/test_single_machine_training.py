# Copyright 2018-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

import pytest
from packaging.version import Version
from sagemaker.huggingface import HuggingFace

from ...integration import ROLE, distilbert_script, distilbert_torch_compiled_script


@pytest.mark.model("hf_bert")
@pytest.mark.integration("hf_local")
@pytest.mark.skip_cpu
@pytest.mark.skip_py2_containers
@pytest.mark.skip_trcomp_containers
@pytest.mark.team("sagemaker-1p-algorithms")
def test_distilbert_base(
    docker_image, processor, instance_type, sagemaker_local_session, py_version, framework_version
):
    if "pytorch" in docker_image and Version(framework_version) < Version("2.2"):
        pytest.skip("Skipping distilbert SM local tests for PT")

    # hyperparameters, which are passed into the training job
    hyperparameters = {
        "max_steps": 5,
        "warmup_steps": 3,
        "train_batch_size": 4,
        "model_name": "distilbert/distilbert-base-uncased",
    }

    estimator = HuggingFace(
        entry_point=distilbert_script,
        instance_type="local_gpu",
        sagemaker_session=sagemaker_local_session,
        image_uri=docker_image,
        instance_count=1,
        role=ROLE,
        py_version=py_version,
        hyperparameters=hyperparameters,
    )

    estimator.fit()


@pytest.mark.model("hf_bert")
@pytest.mark.integration("hf_local")
@pytest.mark.skip_cpu
@pytest.mark.skip_py2_containers
@pytest.mark.skip_trcomp_containers
@pytest.mark.team("sagemaker-1p-algorithms")
def test_distilbert_base_torch_compiled(
    docker_image, processor, instance_type, sagemaker_local_session, py_version, framework_version
):
    if "pytorch" in docker_image and Version(framework_version) < Version("2.2"):
        pytest.skip("Skipping torch compile tests for PT")

    # hyperparameters, which are passed into the training job
    hyperparameters = {
        "max_steps": 5,
        "warmup_steps": 3,
        "train_batch_size": 4,
        "model_name": "distilbert/distilbert-base-uncased",
    }

    estimator = HuggingFace(
        entry_point=distilbert_torch_compiled_script,
        instance_type="local_gpu",
        sagemaker_session=sagemaker_local_session,
        image_uri=docker_image,
        instance_count=1,
        role=ROLE,
        py_version=py_version,
        hyperparameters=hyperparameters,
    )

    estimator.fit()
