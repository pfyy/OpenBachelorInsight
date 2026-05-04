import "frida-il2cpp-bridge";


Il2Cpp.perform(
    function () {
        function get_enemy_count_dict(enemy_lst: Il2Cpp.Object) {
            const enemy_count_dict = new Map<string, number>();

            const cnt = enemy_lst.method("get_Count").invoke() as number;
            for (let i = 0; i < cnt; ++i) {
                const enemy = enemy_lst.method("get_Item").invoke(i) as Il2Cpp.Object;
                const enemy_id = (enemy.field("enemyId").value as Il2Cpp.String).content as string;
                const enemy_cnt = enemy.field("count").value as number;

                enemy_count_dict.set(enemy_id, enemy_cnt);
            }

            return enemy_count_dict;
        }

        function merge_left_right_enemy_count_dict(left_enemy_count_dict: Map<string, number>, right_enemy_count_dict: Map<string, number>) {
            const enemy_count_dict = new Map(left_enemy_count_dict);

            for (const [k, v] of right_enemy_count_dict) {
                enemy_count_dict.set(k, -v);
            }

            return enemy_count_dict;
        }


        Il2Cpp.domain.assembly("Assembly-CSharp").image.class("Torappu.DataCenter.EnemyDuelDataCenter").method("AddTeamData").implementation = function (teamData) {
            const ret = this.method("AddTeamData").invoke(teamData);

            const left_enemy_count_dict = get_enemy_count_dict((teamData as Il2Cpp.Object).field("teamLeft").value as Il2Cpp.Object);
            const right_enemy_count_dict = get_enemy_count_dict((teamData as Il2Cpp.Object).field("teamRight").value as Il2Cpp.Object);

            const enemy_count_dict = merge_left_right_enemy_count_dict(left_enemy_count_dict, right_enemy_count_dict);

            send(Object.fromEntries(enemy_count_dict));

            return ret;
        }
    }
)