import React, { useEffect, useState } from "react";
import { getMachines, getQueue } from "../utils/endpoints";
import MachineCard from "./machine-card";

interface IMachinesPage {}

const MachinesPage: React.FC<IMachinesPage> = () => {
  const [machines, setMachines] = useState<any>([]);

  useEffect(() => {
    getMachines().then((res) => {
      setMachines(res);
    });
  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        alignItems: "center",
        marginTop: 50,
      }}
    >
      {machines?.length > 0 &&
        machines.map((m: any) => <MachineCard id={m[0]} name={m[1]} />)}
    </div>
  );
};

export default MachinesPage;
