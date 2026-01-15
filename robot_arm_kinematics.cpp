/**
 * 机械臂正运动学与逆运动学程序
 * 使用DH参数法（Denavit-Hartenberg）
 *
 * 正运动学：根据关节角度计算末端位置
 * 逆运动学：根据末端位置计算关节角度
 */

#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

using namespace std;

const double PI = 3.14159265358979323846;
const double EPSILON = 1e-6;

// 4x4齐次变换矩阵
class Matrix4x4 {
public:
    double data[4][4];

    Matrix4x4() {
        // 初始化为单位矩阵
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                data[i][j] = (i == j) ? 1.0 : 0.0;
            }
        }
    }

    // 矩阵乘法
    Matrix4x4 operator*(const Matrix4x4& other) const {
        Matrix4x4 result;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                result.data[i][j] = 0;
                for (int k = 0; k < 4; k++) {
                    result.data[i][j] += data[i][k] * other.data[k][j];
                }
            }
        }
        return result;
    }

    // 矩阵转置
    Matrix4x4 transpose() const {
        Matrix4x4 result;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                result.data[i][j] = data[j][i];
            }
        }
        return result;
    }

    // 打印矩阵
    void print() const {
        cout << fixed << setprecision(4);
        for (int i = 0; i < 4; i++) {
            cout << "| ";
            for (int j = 0; j < 4; j++) {
                cout << setw(10) << data[i][j] << " ";
            }
            cout << "|" << endl;
        }
    }
};

// 3D向量类
class Vector3 {
public:
    double x, y, z;

    Vector3(double _x = 0, double _y = 0, double _z = 0) : x(_x), y(_y), z(_z) {}

    double norm() const {
        return sqrt(x * x + y * y + z * z);
    }

    Vector3 operator-(const Vector3& other) const {
        return Vector3(x - other.x, y - other.y, z - other.z);
    }

    void print() const {
        cout << "(" << x << ", " << y << ", " << z << ")" << endl;
    }
};

// DH参数结构体
struct DHParameter {
    double theta;  // 关节角度 (弧度)
    double d;      // 连杆偏距
    double a;      // 连杆长度
    double alpha;  // 连杆扭角 (弧度)
};

// 关节角度结构体（用于逆运动学结果）
struct JointAngles {
    double q1, q2, q3, q4, q5, q6;
    bool valid;  // 是否为有效解

    JointAngles() : q1(0), q2(0), q3(0), q4(0), q5(0), q6(0), valid(false) {}
};

// 角度转弧度
double degToRad(double deg) {
    return deg * PI / 180.0;
}

// 弧度转角度
double radToDeg(double rad) {
    return rad * 180.0 / PI;
}

// 归一化角度到 [-PI, PI]
double normalizeAngle(double angle) {
    while (angle > PI) angle -= 2 * PI;
    while (angle < -PI) angle += 2 * PI;
    return angle;
}

// 安全的atan2
double safeAtan2(double y, double x) {
    if (fabs(x) < EPSILON && fabs(y) < EPSILON) {
        return 0;
    }
    return atan2(y, x);
}

// 安全的acos
double safeAcos(double x) {
    if (x >= 1.0) return 0;
    if (x <= -1.0) return PI;
    return acos(x);
}

// 机械臂类
class RobotArm {
private:
    vector<DHParameter> dhParams;
    int numJoints;

public:
    // 连杆参数（公开以便逆运动学使用）
    double d1, a2, a3, d4, d5, d6;

    RobotArm(int joints = 6) : numJoints(joints) {
        dhParams.resize(joints);
        // 默认连杆参数
        d1 = 0.1;   // 基座高度
        a2 = 0.4;   // 大臂长度
        a3 = 0.3;   // 小臂长度
        d4 = 0.1;   // 手腕偏距
        d5 = 0.0;
        d6 = 0.05;  // 末端工具长度
    }

    // 设置连杆参数
    void setLinkParams(double _d1, double _a2, double _a3, double _d4, double _d6) {
        d1 = _d1;
        a2 = _a2;
        a3 = _a3;
        d4 = _d4;
        d6 = _d6;
    }

    // 设置DH参数
    void setDHParams(int joint, double theta, double d, double a, double alpha) {
        if (joint >= 0 && joint < numJoints) {
            dhParams[joint].theta = theta;
            dhParams[joint].d = d;
            dhParams[joint].a = a;
            dhParams[joint].alpha = alpha;
        }
    }

    // 更新关节角度
    void setJointAngle(int joint, double angle) {
        if (joint >= 0 && joint < numJoints) {
            dhParams[joint].theta = angle;
        }
    }

    // 设置所有关节角度
    void setAllJointAngles(double q1, double q2, double q3, double q4, double q5, double q6) {
        dhParams[0].theta = q1;
        dhParams[1].theta = q2;
        dhParams[2].theta = q3;
        dhParams[3].theta = q4;
        dhParams[4].theta = q5;
        dhParams[5].theta = q6;
    }

    // 初始化DH参数（使用当前连杆参数）
    void initDHParams(double q1, double q2, double q3, double q4, double q5, double q6) {
        setDHParams(0, q1, d1, 0,  degToRad(-90));  // 关节1
        setDHParams(1, q2, 0,  a2, 0);              // 关节2
        setDHParams(2, q3, 0,  a3, 0);              // 关节3
        setDHParams(3, q4, d4, 0,  degToRad(-90));  // 关节4
        setDHParams(4, q5, 0,  0,  degToRad(90));   // 关节5
        setDHParams(5, q6, d6, 0,  0);              // 关节6
    }

    // 计算单个关节的变换矩阵
    Matrix4x4 computeTransformMatrix(const DHParameter& dh) {
        Matrix4x4 T;

        double ct = cos(dh.theta);
        double st = sin(dh.theta);
        double ca = cos(dh.alpha);
        double sa = sin(dh.alpha);

        // 标准DH变换矩阵
        T.data[0][0] = ct;
        T.data[0][1] = -st * ca;
        T.data[0][2] = st * sa;
        T.data[0][3] = dh.a * ct;

        T.data[1][0] = st;
        T.data[1][1] = ct * ca;
        T.data[1][2] = -ct * sa;
        T.data[1][3] = dh.a * st;

        T.data[2][0] = 0;
        T.data[2][1] = sa;
        T.data[2][2] = ca;
        T.data[2][3] = dh.d;

        T.data[3][0] = 0;
        T.data[3][1] = 0;
        T.data[3][2] = 0;
        T.data[3][3] = 1;

        return T;
    }

    // 正运动学计算 - 返回末端执行器的位姿矩阵
    Matrix4x4 forwardKinematics() {
        Matrix4x4 T;  // 单位矩阵

        for (int i = 0; i < numJoints; i++) {
            Matrix4x4 Ti = computeTransformMatrix(dhParams[i]);
            T = T * Ti;
        }

        return T;
    }

    // 使用给定关节角度计算正运动学
    Matrix4x4 forwardKinematics(double q1, double q2, double q3, double q4, double q5, double q6) {
        initDHParams(q1, q2, q3, q4, q5, q6);
        return forwardKinematics();
    }

    // 获取末端位置
    void getEndEffectorPosition(double& x, double& y, double& z) {
        Matrix4x4 T = forwardKinematics();
        x = T.data[0][3];
        y = T.data[1][3];
        z = T.data[2][3];
    }

    // =====================================================
    // 逆运动学实现（解析解法 - 针对6轴机械臂）
    // =====================================================

    /**
     * 逆运动学求解 - 几何解析法
     *
     * 输入：目标位置 (px, py, pz) 和目标姿态（欧拉角 roll, pitch, yaw）
     * 输出：关节角度
     *
     * 注意：6轴机械臂通常有多组解（最多8组），这里返回一组解
     */
    JointAngles inverseKinematics(double px, double py, double pz,
                                   double roll, double pitch, double yaw) {
        JointAngles result;
        result.valid = false;

        // 计算目标旋转矩阵（ZYX欧拉角）
        double cr = cos(roll), sr = sin(roll);
        double cp = cos(pitch), sp = sin(pitch);
        double cy = cos(yaw), sy = sin(yaw);

        Matrix4x4 R;
        R.data[0][0] = cy * cp;
        R.data[0][1] = cy * sp * sr - sy * cr;
        R.data[0][2] = cy * sp * cr + sy * sr;
        R.data[1][0] = sy * cp;
        R.data[1][1] = sy * sp * sr + cy * cr;
        R.data[1][2] = sy * sp * cr - cy * sr;
        R.data[2][0] = -sp;
        R.data[2][1] = cp * sr;
        R.data[2][2] = cp * cr;

        // 计算手腕中心位置（减去末端工具长度）
        double wx = px - d6 * R.data[0][2];
        double wy = py - d6 * R.data[1][2];
        double wz = pz - d6 * R.data[2][2];

        // ========== 求解 q1 ==========
        // 基座旋转角度
        result.q1 = safeAtan2(wy, wx);

        // 处理手腕偏距 d4
        double r = sqrt(wx * wx + wy * wy);
        if (r > EPSILON) {
            double alpha = safeAtan2(d4, sqrt(r * r - d4 * d4));
            // 可以选择 +alpha 或 -alpha（两种解）
            result.q1 = safeAtan2(wy, wx) - alpha;
        }

        // ========== 求解 q2 和 q3 ==========
        // 计算手腕在基座坐标系中相对于关节2的位置
        double s1 = sin(result.q1);
        double c1 = cos(result.q1);

        // 手腕位置相对于关节2原点
        double wx2 = c1 * wx + s1 * wy;
        double wy2 = -s1 * wx + c1 * wy;
        double wz2 = wz - d1;

        // 考虑d4偏距后的投影距离
        double r_xy = sqrt(wx2 * wx2 + wy2 * wy2);
        double s = wz2;  // z方向距离
        double r_proj = sqrt((r_xy - d4) * (r_xy - d4) + s * s);

        // 使用余弦定理求q3
        double cos_q3 = (r_proj * r_proj - a2 * a2 - a3 * a3) / (2 * a2 * a3);

        if (fabs(cos_q3) > 1.0 + EPSILON) {
            // 目标点不可达
            cout << "警告：目标点超出工作空间！" << endl;
            return result;
        }

        cos_q3 = max(-1.0, min(1.0, cos_q3));  // 限制范围
        result.q3 = safeAcos(cos_q3);  // 肘部向上解
        // result.q3 = -safeAcos(cos_q3);  // 肘部向下解（另一组解）

        // 求解q2
        double beta = safeAtan2(s, r_xy - d4);
        double phi = safeAtan2(a3 * sin(result.q3), a2 + a3 * cos(result.q3));
        result.q2 = beta - phi;

        // ========== 求解 q4, q5, q6（手腕姿态）==========
        // 计算前三个关节的旋转矩阵
        Matrix4x4 T03 = forwardKinematics3(result.q1, result.q2, result.q3);

        // R36 = R03^T * R06
        // 提取R03的旋转部分并转置
        double R03_00 = T03.data[0][0], R03_01 = T03.data[0][1], R03_02 = T03.data[0][2];
        double R03_10 = T03.data[1][0], R03_11 = T03.data[1][1], R03_12 = T03.data[1][2];
        double R03_20 = T03.data[2][0], R03_21 = T03.data[2][1], R03_22 = T03.data[2][2];

        // 目标旋转矩阵
        double R06_00 = R.data[0][0], R06_01 = R.data[0][1], R06_02 = R.data[0][2];
        double R06_10 = R.data[1][0], R06_11 = R.data[1][1], R06_12 = R.data[1][2];
        double R06_20 = R.data[2][0], R06_21 = R.data[2][1], R06_22 = R.data[2][2];

        // R36 = R03^T * R06
        double R36_00 = R03_00*R06_00 + R03_10*R06_10 + R03_20*R06_20;
        double R36_01 = R03_00*R06_01 + R03_10*R06_11 + R03_20*R06_21;
        double R36_02 = R03_00*R06_02 + R03_10*R06_12 + R03_20*R06_22;
        double R36_10 = R03_01*R06_00 + R03_11*R06_10 + R03_21*R06_20;
        double R36_11 = R03_01*R06_01 + R03_11*R06_11 + R03_21*R06_21;
        double R36_12 = R03_01*R06_02 + R03_11*R06_12 + R03_21*R06_22;
        double R36_20 = R03_02*R06_00 + R03_12*R06_10 + R03_22*R06_20;
        double R36_21 = R03_02*R06_01 + R03_12*R06_11 + R03_22*R06_21;
        double R36_22 = R03_02*R06_02 + R03_12*R06_12 + R03_22*R06_22;

        // 从R36提取ZYZ欧拉角（对应q4, q5, q6）
        if (fabs(R36_22) < 1.0 - EPSILON) {
            result.q5 = safeAcos(R36_22);
            result.q4 = safeAtan2(R36_12, R36_02);
            result.q6 = safeAtan2(R36_21, -R36_20);
        } else {
            // 奇异位置（q5 = 0 或 PI）
            result.q5 = (R36_22 > 0) ? 0 : PI;
            result.q4 = 0;
            result.q6 = safeAtan2(-R36_01, R36_00);
        }

        // 归一化角度
        result.q1 = normalizeAngle(result.q1);
        result.q2 = normalizeAngle(result.q2);
        result.q3 = normalizeAngle(result.q3);
        result.q4 = normalizeAngle(result.q4);
        result.q5 = normalizeAngle(result.q5);
        result.q6 = normalizeAngle(result.q6);

        result.valid = true;
        return result;
    }

    /**
     * 简化版逆运动学 - 仅位置（3自由度）
     * 适用于只关心末端位置而不关心姿态的场景
     */
    JointAngles inverseKinematicsPosition(double px, double py, double pz) {
        JointAngles result;
        result.valid = false;

        // ========== 求解 q1 ==========
        result.q1 = safeAtan2(py, px);

        // ========== 求解 q2 和 q3 ==========
        double c1 = cos(result.q1);
        double s1 = sin(result.q1);

        // 计算目标点在关节2坐标系中的位置
        double x = c1 * px + s1 * py;
        double z = pz - d1 - d6;  // 减去基座高度和末端长度

        // 到关节2的距离
        double D = sqrt(x * x + z * z);

        // 检查是否可达
        if (D > a2 + a3 || D < fabs(a2 - a3)) {
            cout << "警告：目标点超出工作空间！" << endl;
            cout << "距离 D = " << D << ", 范围 [" << fabs(a2-a3) << ", " << a2+a3 << "]" << endl;
            return result;
        }

        // 使用余弦定理求q3
        double cos_q3 = (D * D - a2 * a2 - a3 * a3) / (2 * a2 * a3);
        cos_q3 = max(-1.0, min(1.0, cos_q3));

        result.q3 = safeAcos(cos_q3);  // 肘部向上

        // 求解q2
        double alpha = safeAtan2(z, x);
        double beta = safeAtan2(a3 * sin(result.q3), a2 + a3 * cos(result.q3));
        result.q2 = alpha - beta;

        // 手腕关节设为0
        result.q4 = 0;
        result.q5 = 0;
        result.q6 = 0;

        // 归一化
        result.q1 = normalizeAngle(result.q1);
        result.q2 = normalizeAngle(result.q2);
        result.q3 = normalizeAngle(result.q3);

        result.valid = true;
        return result;
    }

    /**
     * 数值迭代法逆运动学（雅可比迭代）
     * 适用于任意构型的机械臂，但可能收敛较慢
     */
    JointAngles inverseKinematicsNumerical(double px, double py, double pz,
                                            double roll, double pitch, double yaw,
                                            int maxIterations = 100,
                                            double tolerance = 1e-4) {
        JointAngles result;
        result.valid = false;

        // 初始猜测（可以使用当前位置或零位）
        double q[6] = {0, 0, 0, 0, 0, 0};

        Vector3 targetPos(px, py, pz);

        for (int iter = 0; iter < maxIterations; iter++) {
            // 计算当前位置
            Matrix4x4 T = forwardKinematics(q[0], q[1], q[2], q[3], q[4], q[5]);
            Vector3 currentPos(T.data[0][3], T.data[1][3], T.data[2][3]);

            // 计算误差
            Vector3 error = targetPos - currentPos;
            double errorNorm = error.norm();

            if (errorNorm < tolerance) {
                // 收敛成功
                result.q1 = normalizeAngle(q[0]);
                result.q2 = normalizeAngle(q[1]);
                result.q3 = normalizeAngle(q[2]);
                result.q4 = normalizeAngle(q[3]);
                result.q5 = normalizeAngle(q[4]);
                result.q6 = normalizeAngle(q[5]);
                result.valid = true;
                cout << "数值法在 " << iter + 1 << " 次迭代后收敛" << endl;
                return result;
            }

            // 计算雅可比矩阵（数值微分）
            double J[3][6];
            double delta = 1e-6;

            for (int j = 0; j < 6; j++) {
                double q_plus[6], q_minus[6];
                for (int k = 0; k < 6; k++) {
                    q_plus[k] = q[k];
                    q_minus[k] = q[k];
                }
                q_plus[j] += delta;
                q_minus[j] -= delta;

                Matrix4x4 T_plus = forwardKinematics(q_plus[0], q_plus[1], q_plus[2],
                                                      q_plus[3], q_plus[4], q_plus[5]);
                Matrix4x4 T_minus = forwardKinematics(q_minus[0], q_minus[1], q_minus[2],
                                                       q_minus[3], q_minus[4], q_minus[5]);

                J[0][j] = (T_plus.data[0][3] - T_minus.data[0][3]) / (2 * delta);
                J[1][j] = (T_plus.data[1][3] - T_minus.data[1][3]) / (2 * delta);
                J[2][j] = (T_plus.data[2][3] - T_minus.data[2][3]) / (2 * delta);
            }

            // 使用伪逆计算关节速度（简化：使用转置代替）
            // dq = J^T * error * gain
            double gain = 0.5;
            for (int j = 0; j < 6; j++) {
                double dq = gain * (J[0][j] * error.x + J[1][j] * error.y + J[2][j] * error.z);
                q[j] += dq;
            }
        }

        cout << "警告：数值法未能在最大迭代次数内收敛" << endl;
        return result;
    }

private:
    // 计算前三个关节的变换矩阵
    Matrix4x4 forwardKinematics3(double q1, double q2, double q3) {
        DHParameter dh1 = {q1, d1, 0, degToRad(-90)};
        DHParameter dh2 = {q2, 0, a2, 0};
        DHParameter dh3 = {q3, 0, a3, 0};

        Matrix4x4 T1 = computeTransformMatrix(dh1);
        Matrix4x4 T2 = computeTransformMatrix(dh2);
        Matrix4x4 T3 = computeTransformMatrix(dh3);

        return T1 * T2 * T3;
    }

public:
    // 打印DH参数表
    void printDHTable() {
        cout << "\nDH参数表:" << endl;
        cout << "---------------------------------------------------" << endl;
        cout << "关节\ttheta(rad)\td\t\ta\t\talpha(rad)" << endl;
        cout << "---------------------------------------------------" << endl;
        for (int i = 0; i < numJoints; i++) {
            cout << i + 1 << "\t"
                 << fixed << setprecision(4)
                 << dhParams[i].theta << "\t\t"
                 << dhParams[i].d << "\t\t"
                 << dhParams[i].a << "\t\t"
                 << dhParams[i].alpha << endl;
        }
        cout << "---------------------------------------------------" << endl;
    }

    // 打印关节角度
    void printJointAngles(const JointAngles& angles) {
        cout << fixed << setprecision(2);
        cout << "关节角度（度）:" << endl;
        cout << "  q1 = " << setw(8) << radToDeg(angles.q1) << "°" << endl;
        cout << "  q2 = " << setw(8) << radToDeg(angles.q2) << "°" << endl;
        cout << "  q3 = " << setw(8) << radToDeg(angles.q3) << "°" << endl;
        cout << "  q4 = " << setw(8) << radToDeg(angles.q4) << "°" << endl;
        cout << "  q5 = " << setw(8) << radToDeg(angles.q5) << "°" << endl;
        cout << "  q6 = " << setw(8) << radToDeg(angles.q6) << "°" << endl;
    }
};

// =====================================================
// 主程序
// =====================================================
int main() {
    cout << "========================================" << endl;
    cout << "   机械臂运动学计算程序（正/逆）" << endl;
    cout << "========================================" << endl;

    // 创建机械臂
    RobotArm arm;

    // 设置连杆参数
    arm.setLinkParams(0.1, 0.4, 0.3, 0.1, 0.05);

    // =====================================================
    // 测试1：正运动学
    // =====================================================
    cout << "\n【测试1】正运动学计算" << endl;
    cout << "----------------------------------------" << endl;

    double q1 = degToRad(30);
    double q2 = degToRad(45);
    double q3 = degToRad(-30);
    double q4 = degToRad(0);
    double q5 = degToRad(60);
    double q6 = degToRad(0);

    cout << "输入关节角度:" << endl;
    cout << "  q1=30°, q2=45°, q3=-30°, q4=0°, q5=60°, q6=0°" << endl;

    Matrix4x4 T = arm.forwardKinematics(q1, q2, q3, q4, q5, q6);

    cout << "\n末端执行器变换矩阵:" << endl;
    T.print();

    double px = T.data[0][3];
    double py = T.data[1][3];
    double pz = T.data[2][3];

    cout << "\n末端位置:" << endl;
    cout << fixed << setprecision(4);
    cout << "  X = " << px << " 米" << endl;
    cout << "  Y = " << py << " 米" << endl;
    cout << "  Z = " << pz << " 米" << endl;

    // =====================================================
    // 测试2：逆运动学（位置）
    // =====================================================
    cout << "\n【测试2】逆运动学计算（仅位置）" << endl;
    cout << "----------------------------------------" << endl;

    // 使用正运动学计算的位置作为目标
    cout << "目标位置: (" << px << ", " << py << ", " << pz << ")" << endl;

    JointAngles ikResult = arm.inverseKinematicsPosition(px, py, pz);

    if (ikResult.valid) {
        cout << "\n逆运动学求解成功！" << endl;
        arm.printJointAngles(ikResult);

        // 验证：用求得的角度进行正运动学计算
        cout << "\n验证（用求得角度计算正运动学）:" << endl;
        Matrix4x4 T_verify = arm.forwardKinematics(ikResult.q1, ikResult.q2, ikResult.q3,
                                                    ikResult.q4, ikResult.q5, ikResult.q6);
        cout << "  计算位置: (" << T_verify.data[0][3] << ", "
             << T_verify.data[1][3] << ", " << T_verify.data[2][3] << ")" << endl;
        cout << "  目标位置: (" << px << ", " << py << ", " << pz << ")" << endl;

        double error = sqrt(pow(T_verify.data[0][3] - px, 2) +
                           pow(T_verify.data[1][3] - py, 2) +
                           pow(T_verify.data[2][3] - pz, 2));
        cout << "  位置误差: " << error << " 米" << endl;
    } else {
        cout << "逆运动学求解失败！" << endl;
    }

    // =====================================================
    // 测试3：逆运动学（位置+姿态）
    // =====================================================
    cout << "\n【测试3】逆运动学计算（位置+姿态）" << endl;
    cout << "----------------------------------------" << endl;

    // 目标位置和姿态
    double target_x = 0.5;
    double target_y = 0.2;
    double target_z = 0.3;
    double target_roll = degToRad(0);
    double target_pitch = degToRad(45);
    double target_yaw = degToRad(30);

    cout << "目标位置: (" << target_x << ", " << target_y << ", " << target_z << ")" << endl;
    cout << "目标姿态: roll=0°, pitch=45°, yaw=30°" << endl;

    JointAngles ikResult2 = arm.inverseKinematics(target_x, target_y, target_z,
                                                   target_roll, target_pitch, target_yaw);

    if (ikResult2.valid) {
        cout << "\n逆运动学求解成功！" << endl;
        arm.printJointAngles(ikResult2);

        // 验证
        Matrix4x4 T_verify2 = arm.forwardKinematics(ikResult2.q1, ikResult2.q2, ikResult2.q3,
                                                     ikResult2.q4, ikResult2.q5, ikResult2.q6);
        cout << "\n验证结果:" << endl;
        cout << "  计算位置: (" << T_verify2.data[0][3] << ", "
             << T_verify2.data[1][3] << ", " << T_verify2.data[2][3] << ")" << endl;
    } else {
        cout << "逆运动学求解失败！" << endl;
    }

    // =====================================================
    // 测试4：数值迭代法
    // =====================================================
    cout << "\n【测试4】数值迭代法逆运动学" << endl;
    cout << "----------------------------------------" << endl;

    double num_target_x = 0.4;
    double num_target_y = 0.3;
    double num_target_z = 0.2;

    cout << "目标位置: (" << num_target_x << ", " << num_target_y << ", " << num_target_z << ")" << endl;

    JointAngles ikResult3 = arm.inverseKinematicsNumerical(num_target_x, num_target_y, num_target_z,
                                                           0, 0, 0);

    if (ikResult3.valid) {
        cout << "数值法求解成功！" << endl;
        arm.printJointAngles(ikResult3);

        // 验证
        Matrix4x4 T_verify3 = arm.forwardKinematics(ikResult3.q1, ikResult3.q2, ikResult3.q3,
                                                     ikResult3.q4, ikResult3.q5, ikResult3.q6);
        double error = sqrt(pow(T_verify3.data[0][3] - num_target_x, 2) +
                           pow(T_verify3.data[1][3] - num_target_y, 2) +
                           pow(T_verify3.data[2][3] - num_target_z, 2));
        cout << "位置误差: " << error << " 米" << endl;
    }

    // =====================================================
    // 测试5：工作空间边界测试
    // =====================================================
    cout << "\n【测试5】工作空间边界测试" << endl;
    cout << "----------------------------------------" << endl;

    // 测试一个超出范围的点
    cout << "测试超出工作空间的点 (1.5, 0, 0):" << endl;
    JointAngles ikFail = arm.inverseKinematicsPosition(1.5, 0, 0);
    if (!ikFail.valid) {
        cout << "正确检测到目标点不可达" << endl;
    }

    cout << "\n========================================" << endl;
    cout << "程序结束" << endl;
    cout << "========================================" << endl;

    return 0;
}
