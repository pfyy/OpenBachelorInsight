import "frida-il2cpp-bridge";


Il2Cpp.perform(
    function () {

        function check_data(data: Il2Cpp.Object) {
            if (data.isNull()) {
                return;
            }

            const randomSpawnGroupKey = data.field("randomSpawnGroupKey").value as Il2Cpp.String;
            const randomSpawnGroupPackKey = data.field("randomSpawnGroupPackKey").value as Il2Cpp.String;

            if (randomSpawnGroupKey.isNull() || randomSpawnGroupPackKey.isNull()) {
                return;
            }

            console.log("randomSpawnGroup:", randomSpawnGroupKey, randomSpawnGroupPackKey);
        }

        Il2Cpp.domain.assembly("Assembly-CSharp").image.class("Torappu.Battle.Scheduler").method("_OnActionExecuted").implementation = function (data) {
            check_data(data as Il2Cpp.Object);

            const ret = this.method("_OnActionExecuted").invoke(data);
            return ret;
        }
    }
)