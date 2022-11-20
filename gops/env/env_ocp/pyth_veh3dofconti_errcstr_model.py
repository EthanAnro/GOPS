#  Copyright (c). All Rights Reserved.
#  General Optimal control Problem Solver (GOPS)
#  Intelligent Driving Lab(iDLab), Tsinghua University
#
#  Creator: iDLab
#  Description: Vehicle 3DOF model environment with tracking error constraint


from typing import Dict, Optional, Tuple, Union

import torch

from gops.env.env_ocp.pyth_veh3dofconti_model import Veh3dofcontiModel
from gops.utils.gops_typing import InfoDict


class Veh3dofcontiErrCstrModel(Veh3dofcontiModel):
    def __init__(
        self,
        pre_horizon: int,
        device: Union[torch.device, str, None] = None,
        path_para: Optional[Dict[str, Dict]] = None,
        u_para: Optional[Dict[str, Dict]] = None,
        y_error_tol: float = 0.2,
        u_error_tol: float = 2.0,
        **kwargs,
    ):
        super().__init__(pre_horizon, device, path_para, u_para)
        self.y_error_tol = y_error_tol
        self.u_error_tol = u_error_tol

    def forward(self, obs: torch.Tensor, action: torch.Tensor, done: torch.Tensor, info: InfoDict) \
            -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, InfoDict]:
        next_obs, reward, next_done, next_info = super().forward(obs, action, done, info)
        info["constraint"] = self.get_constraint(obs)
        return next_obs, reward, next_done, next_info

    def get_constraint(self, obs: torch.Tensor) -> torch.Tensor:
        y_error = obs[:, 1]
        u_error = obs[:, 3]
        constraint = torch.stack((y_error.abs() - self.y_error_tol, u_error.abs() - self.u_error_tol), dim=1)
        return constraint


def env_model_creator(**kwargs):
    return Veh3dofcontiErrCstrModel(**kwargs)
